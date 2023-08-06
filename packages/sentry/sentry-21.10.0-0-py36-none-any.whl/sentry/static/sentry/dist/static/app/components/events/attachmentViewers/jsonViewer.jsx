Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const contextData_1 = (0, tslib_1.__importDefault)(require("app/components/contextData"));
const previewPanelItem_1 = (0, tslib_1.__importDefault)(require("app/components/events/attachmentViewers/previewPanelItem"));
const utils_1 = require("app/components/events/attachmentViewers/utils");
class JsonViewer extends asyncComponent_1.default {
    getEndpoints() {
        return [['attachmentJson', (0, utils_1.getAttachmentUrl)(this.props)]];
    }
    renderBody() {
        const { attachmentJson } = this.state;
        if (!attachmentJson) {
            return null;
        }
        let json;
        try {
            json = JSON.parse(attachmentJson);
        }
        catch (e) {
            json = null;
        }
        return (<previewPanelItem_1.default>
        <StyledContextData data={json} maxDefaultDepth={4} preserveQuotes style={{ width: '100%' }} jsonConsts/>
      </previewPanelItem_1.default>);
    }
}
exports.default = JsonViewer;
const StyledContextData = (0, styled_1.default)(contextData_1.default) `
  margin-bottom: 0;
`;
//# sourceMappingURL=jsonViewer.jsx.map