Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const uniq_1 = (0, tslib_1.__importDefault)(require("lodash/uniq"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const locale_1 = require("app/locale");
const ownerInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectOwnership/ownerInput"));
class ProjectOwnershipModal extends asyncComponent_1.default {
    getEndpoints() {
        const { organization, project, issueId } = this.props;
        return [
            ['ownership', `/projects/${organization.slug}/${project.slug}/ownership/`],
            [
                'urlTagData',
                `/issues/${issueId}/tags/url/`,
                {},
                {
                    allowError: error => 
                    // Allow for 404s
                    error.status === 404,
                },
            ],
            ['eventData', `/issues/${issueId}/events/latest/`],
        ];
    }
    renderBody() {
        var _a, _b, _c, _d, _e, _f, _g;
        const { ownership, urlTagData, eventData } = this.state;
        if (!ownership && !urlTagData && !eventData) {
            return null;
        }
        const urls = urlTagData
            ? urlTagData.topValues
                .sort((a, b) => a.count - b.count)
                .map(i => i.value)
                .slice(0, 5)
            : [];
        // pull frame data out of exception or the stacktrace
        const entry = (eventData === null || eventData === void 0 ? void 0 : eventData.entries).find(({ type }) => ['exception', 'stacktrace'].includes(type));
        let frames = [];
        if ((entry === null || entry === void 0 ? void 0 : entry.type) === 'exception') {
            frames = (_e = (_d = (_c = (_b = (_a = entry === null || entry === void 0 ? void 0 : entry.data) === null || _a === void 0 ? void 0 : _a.values) === null || _b === void 0 ? void 0 : _b[0]) === null || _c === void 0 ? void 0 : _c.stacktrace) === null || _d === void 0 ? void 0 : _d.frames) !== null && _e !== void 0 ? _e : [];
        }
        if ((entry === null || entry === void 0 ? void 0 : entry.type) === 'stacktrace') {
            frames = (_g = (_f = entry === null || entry === void 0 ? void 0 : entry.data) === null || _f === void 0 ? void 0 : _f.frames) !== null && _g !== void 0 ? _g : [];
        }
        // filter frames by inApp unless there would be 0
        const inAppFrames = frames.filter(frame => frame.inApp);
        if (inAppFrames.length > 0) {
            frames = inAppFrames;
        }
        const paths = (0, uniq_1.default)(frames.map(frame => frame.filename || frame.absPath || ''))
            .filter(i => i)
            .slice(0, 30);
        return (<react_1.Fragment>
        <p>{(0, locale_1.t)('Match against Issue Data: (globbing syntax *, ? supported)')}</p>
        <ownerInput_1.default {...this.props} initialText={(ownership === null || ownership === void 0 ? void 0 : ownership.raw) || ''} urls={urls} paths={paths}/>
      </react_1.Fragment>);
    }
}
exports.default = ProjectOwnershipModal;
//# sourceMappingURL=modal.jsx.map