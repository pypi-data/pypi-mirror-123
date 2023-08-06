Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const guideActions_1 = (0, tslib_1.__importDefault)(require("app/actions/guideActions"));
const organizationsActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationsActions"));
const api_1 = require("app/api");
const getGuidesContent_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/getGuidesContent"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const analytics_1 = require("app/utils/analytics");
function guidePrioritySort(a, b) {
    var _a, _b;
    const a_priority = (_a = a.priority) !== null && _a !== void 0 ? _a : Number.MAX_SAFE_INTEGER;
    const b_priority = (_b = b.priority) !== null && _b !== void 0 ? _b : Number.MAX_SAFE_INTEGER;
    if (a_priority === b_priority) {
        return a.guide.localeCompare(b.guide);
    }
    // lower number takes priority
    return a_priority - b_priority;
}
const defaultState = {
    guides: [],
    anchors: new Set(),
    currentGuide: null,
    currentStep: 0,
    orgId: null,
    orgSlug: null,
    forceShow: false,
    prevGuide: null,
};
const storeConfig = {
    state: defaultState,
    init() {
        this.state = defaultState;
        this.api = new api_1.Client();
        this.listenTo(guideActions_1.default.fetchSucceeded, this.onFetchSucceeded);
        this.listenTo(guideActions_1.default.closeGuide, this.onCloseGuide);
        this.listenTo(guideActions_1.default.nextStep, this.onNextStep);
        this.listenTo(guideActions_1.default.toStep, this.onToStep);
        this.listenTo(guideActions_1.default.registerAnchor, this.onRegisterAnchor);
        this.listenTo(guideActions_1.default.unregisterAnchor, this.onUnregisterAnchor);
        this.listenTo(organizationsActions_1.default.setActive, this.onSetActiveOrganization);
        window.addEventListener('load', this.onURLChange, false);
        react_router_1.browserHistory.listen(() => this.onURLChange());
    },
    onURLChange() {
        this.state.forceShow = window.location.hash === '#assistant';
        this.updateCurrentGuide();
    },
    onSetActiveOrganization(data) {
        this.state.orgId = data ? data.id : null;
        this.state.orgSlug = data ? data.slug : null;
        this.updateCurrentGuide();
    },
    onFetchSucceeded(data) {
        // It's possible we can get empty responses (seems to be Firefox specific)
        // Do nothing if `data` is empty
        // also, temporarily check data is in the correct format from the updated
        // assistant endpoint
        if (!data || !Array.isArray(data)) {
            return;
        }
        const guidesContent = (0, getGuidesContent_1.default)(this.state.orgSlug);
        // map server guide state (i.e. seen status) with guide content
        const guides = guidesContent.reduce((acc, content) => {
            const serverGuide = data.find(guide => guide.guide === content.guide);
            serverGuide &&
                acc.push(Object.assign(Object.assign({}, content), serverGuide));
            return acc;
        }, []);
        this.state.guides = guides;
        this.updateCurrentGuide();
    },
    onCloseGuide(dismissed) {
        const { currentGuide, guides } = this.state;
        // update the current guide seen to true or all guides
        // if markOthersAsSeen is true and the user is dismissing
        guides
            .filter(guide => guide.guide === (currentGuide === null || currentGuide === void 0 ? void 0 : currentGuide.guide) ||
            ((currentGuide === null || currentGuide === void 0 ? void 0 : currentGuide.markOthersAsSeen) && dismissed))
            .forEach(guide => (guide.seen = true));
        this.state.forceShow = false;
        this.updateCurrentGuide();
    },
    onNextStep() {
        this.state.currentStep += 1;
        this.trigger(this.state);
    },
    onToStep(step) {
        this.state.currentStep = step;
        this.trigger(this.state);
    },
    onRegisterAnchor(target) {
        this.state.anchors.add(target);
        this.updateCurrentGuide();
    },
    onUnregisterAnchor(target) {
        this.state.anchors.delete(target);
        this.updateCurrentGuide();
    },
    recordCue(guide) {
        const user = configStore_1.default.get('user');
        if (!user) {
            return;
        }
        const data = {
            guide,
            eventKey: 'assistant.guide_cued',
            eventName: 'Assistant Guide Cued',
            organization_id: this.state.orgId,
            user_id: parseInt(user.id, 10),
        };
        (0, analytics_1.trackAnalyticsEvent)(data);
    },
    updatePrevGuide(nextGuide) {
        const { prevGuide } = this.state;
        if (!nextGuide) {
            return;
        }
        if (!prevGuide || prevGuide.guide !== nextGuide.guide) {
            this.recordCue(nextGuide.guide);
            this.state.prevGuide = nextGuide;
        }
    },
    /**
     * Logic to determine if a guide is shown:
     *
     *  - If any required target is missing, don't show the guide
     *  - If the URL ends with #assistant, show the guide
     *  - If the user has already seen the guide, don't show the guide
     *  - Otherwise show the guide
     */
    updateCurrentGuide() {
        const { anchors, guides, forceShow } = this.state;
        let guideOptions = guides
            .sort(guidePrioritySort)
            .filter(guide => guide.requiredTargets.every(target => anchors.has(target)));
        const user = configStore_1.default.get('user');
        const assistantThreshold = new Date(2019, 6, 1);
        const userDateJoined = new Date(user === null || user === void 0 ? void 0 : user.dateJoined);
        if (!forceShow) {
            guideOptions = guideOptions.filter(({ seen, dateThreshold }) => {
                if (seen) {
                    return false;
                }
                else if (user === null || user === void 0 ? void 0 : user.isSuperuser) {
                    return true;
                }
                else if (dateThreshold) {
                    // Show the guide to users who've joined before the date threshold
                    return userDateJoined < dateThreshold;
                }
                else {
                    return userDateJoined > assistantThreshold;
                }
            });
        }
        const nextGuide = guideOptions.length > 0
            ? Object.assign(Object.assign({}, guideOptions[0]), { steps: guideOptions[0].steps.filter(step => step.target && anchors.has(step.target)) }) : null;
        this.updatePrevGuide(nextGuide);
        this.state.currentStep =
            this.state.currentGuide &&
                nextGuide &&
                this.state.currentGuide.guide === nextGuide.guide
                ? this.state.currentStep
                : 0;
        this.state.currentGuide = nextGuide;
        this.trigger(this.state);
    },
};
const GuideStore = reflux_1.default.createStore(storeConfig);
exports.default = GuideStore;
//# sourceMappingURL=guideStore.jsx.map