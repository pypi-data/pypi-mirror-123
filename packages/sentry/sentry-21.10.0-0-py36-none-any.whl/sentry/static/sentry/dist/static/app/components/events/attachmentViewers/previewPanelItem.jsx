Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const PreviewPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  overflow: auto;
  max-height: 500px;
  padding: 0;
`;
exports.default = PreviewPanelItem;
//# sourceMappingURL=previewPanelItem.jsx.map