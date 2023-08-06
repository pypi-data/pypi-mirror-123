Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const imageViewer_1 = (0, tslib_1.__importDefault)(require("app/components/events/attachmentViewers/imageViewer"));
const ImageVisualization = (0, styled_1.default)(imageViewer_1.default) `
  padding: 0;
  height: 100%;
  img {
    width: auto;
    height: 100%;
    object-fit: cover;
    flex: 1;
  }
`;
exports.default = ImageVisualization;
//# sourceMappingURL=imageVisualization.jsx.map