Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const lazyLoad_1 = (0, tslib_1.__importDefault)(require("app/components/lazyLoad"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class RRWebIntegration extends asyncComponent_1.default {
    getEndpoints() {
        const { orgId, projectId, event } = this.props;
        return [
            [
                'attachmentList',
                `/projects/${orgId}/${projectId}/events/${event.id}/attachments/`,
                { query: { query: 'rrweb.json' } },
            ],
        ];
    }
    renderLoading() {
        // hide loading indicator
        return null;
    }
    renderBody() {
        const { attachmentList } = this.state;
        if (!(attachmentList === null || attachmentList === void 0 ? void 0 : attachmentList.length)) {
            return null;
        }
        const attachment = attachmentList[0];
        const { orgId, projectId, event } = this.props;
        return (<StyledEventDataSection type="context-replay" title={(0, locale_1.t)('Replay')}>
        <lazyLoad_1.default component={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('./rrwebReplayer')))} url={`/api/0/projects/${orgId}/${projectId}/events/${event.id}/attachments/${attachment.id}/?download`}/>
      </StyledEventDataSection>);
    }
}
const StyledEventDataSection = (0, styled_1.default)(eventDataSection_1.default) `
  overflow: hidden;
  margin-bottom: ${(0, space_1.default)(3)};
`;
exports.default = RRWebIntegration;
//# sourceMappingURL=rrwebIntegration.jsx.map