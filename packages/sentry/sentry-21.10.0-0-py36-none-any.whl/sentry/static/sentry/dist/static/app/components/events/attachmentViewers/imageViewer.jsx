Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("app/components/events/attachmentViewers/utils");
const panels_1 = require("app/components/panels");
function ImageViewer(_a) {
    var { className } = _a, props = (0, tslib_1.__rest)(_a, ["className"]);
    return (<Container className={className}>
      <img src={(0, utils_1.getAttachmentUrl)(props, true)}/>
    </Container>);
}
exports.default = ImageViewer;
const Container = (0, styled_1.default)(panels_1.PanelItem) `
  justify-content: center;
`;
//# sourceMappingURL=imageViewer.jsx.map