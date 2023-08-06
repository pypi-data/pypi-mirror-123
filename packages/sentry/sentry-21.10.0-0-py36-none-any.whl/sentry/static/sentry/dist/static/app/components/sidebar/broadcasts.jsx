Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const broadcasts_1 = require("app/actionCreators/broadcasts");
const demoModeGate_1 = (0, tslib_1.__importDefault)(require("app/components/acl/demoModeGate"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const broadcastSdkUpdates_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/broadcastSdkUpdates"));
const sidebarItem_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarItem"));
const sidebarPanel_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarPanel"));
const sidebarPanelEmpty_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarPanelEmpty"));
const sidebarPanelItem_1 = (0, tslib_1.__importDefault)(require("app/components/sidebar/sidebarPanelItem"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const types_1 = require("./types");
const MARK_SEEN_DELAY = 1000;
const POLLER_DELAY = 600000; // 10 minute poll (60 * 10 * 1000)
class Broadcasts extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            broadcasts: [],
            loading: true,
            error: false,
        };
        this.poller = null;
        this.timer = null;
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (this.poller) {
                this.stopPoll();
            }
            try {
                const data = yield (0, broadcasts_1.getAllBroadcasts)(this.props.api, this.props.organization.slug);
                this.setState({ loading: false, broadcasts: data || [] });
            }
            catch (_a) {
                this.setState({ loading: false, error: true });
            }
            this.startPoll();
        });
        /**
         * If tab/window loses visibility (note: this is different than focus), stop
         * polling for broadcasts data, otherwise, if it gains visibility, start
         * polling again.
         */
        this.handleVisibilityChange = () => (document.hidden ? this.stopPoll() : this.startPoll());
        this.handleShowPanel = () => {
            this.timer = window.setTimeout(this.markSeen, MARK_SEEN_DELAY);
            this.props.onShowPanel();
        };
        this.markSeen = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const unseenBroadcastIds = this.unseenIds;
            if (unseenBroadcastIds.length === 0) {
                return;
            }
            yield (0, broadcasts_1.markBroadcastsAsSeen)(this.props.api, unseenBroadcastIds);
            this.setState(state => ({
                broadcasts: state.broadcasts.map(item => (Object.assign(Object.assign({}, item), { hasSeen: true }))),
            }));
        });
    }
    componentDidMount() {
        this.fetchData();
        document.addEventListener('visibilitychange', this.handleVisibilityChange);
    }
    componentWillUnmount() {
        if (this.timer) {
            window.clearTimeout(this.timer);
            this.timer = null;
        }
        if (this.poller) {
            this.stopPoll();
        }
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
    }
    startPoll() {
        this.poller = window.setTimeout(this.fetchData, POLLER_DELAY);
    }
    stopPoll() {
        if (this.poller) {
            window.clearTimeout(this.poller);
            this.poller = null;
        }
    }
    get unseenIds() {
        return this.state.broadcasts
            ? this.state.broadcasts.filter(item => !item.hasSeen).map(item => item.id)
            : [];
    }
    render() {
        const { orientation, collapsed, currentPanel, hidePanel } = this.props;
        const { broadcasts, loading } = this.state;
        const unseenPosts = this.unseenIds;
        return (<demoModeGate_1.default>
        <react_1.Fragment>
          <sidebarItem_1.default data-test-id="sidebar-broadcasts" orientation={orientation} collapsed={collapsed} active={currentPanel === types_1.SidebarPanelKey.Broadcasts} badge={unseenPosts.length} icon={<icons_1.IconBroadcast size="md"/>} label={(0, locale_1.t)("What's new")} onClick={this.handleShowPanel} id="broadcasts"/>

          {currentPanel === types_1.SidebarPanelKey.Broadcasts && (<sidebarPanel_1.default data-test-id="sidebar-broadcasts-panel" orientation={orientation} collapsed={collapsed} title={(0, locale_1.t)("What's new in Sentry")} hidePanel={hidePanel}>
              {loading ? (<loadingIndicator_1.default />) : broadcasts.length === 0 ? (<sidebarPanelEmpty_1.default>
                  {(0, locale_1.t)('No recent updates from the Sentry team.')}
                </sidebarPanelEmpty_1.default>) : (broadcasts.map(item => (<sidebarPanelItem_1.default key={item.id} hasSeen={item.hasSeen} title={item.title} message={item.message} link={item.link} cta={item.cta}/>)))}
              <broadcastSdkUpdates_1.default />
            </sidebarPanel_1.default>)}
        </react_1.Fragment>
      </demoModeGate_1.default>);
    }
}
exports.default = (0, withApi_1.default)(Broadcasts);
//# sourceMappingURL=broadcasts.jsx.map