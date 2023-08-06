Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const ansicolor_1 = (0, tslib_1.__importDefault)(require("ansicolor"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const previewPanelItem_1 = (0, tslib_1.__importDefault)(require("app/components/events/attachmentViewers/previewPanelItem"));
const utils_1 = require("app/components/events/attachmentViewers/utils");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const COLORS = {
    black: theme_1.default.black,
    white: theme_1.default.white,
    redDim: theme_1.default.red200,
    red: theme_1.default.red300,
    greenDim: theme_1.default.green200,
    green: theme_1.default.green300,
    yellowDim: theme_1.default.yellow300,
    yellow: theme_1.default.orange300,
    blueDim: theme_1.default.blue200,
    blue: theme_1.default.blue300,
    magentaDim: theme_1.default.pink200,
    magenta: theme_1.default.pink300,
    cyanDim: theme_1.default.blue200,
    cyan: theme_1.default.blue300,
};
class LogFileViewer extends asyncComponent_1.default {
    getEndpoints() {
        return [['attachmentText', (0, utils_1.getAttachmentUrl)(this.props)]];
    }
    renderBody() {
        const { attachmentText } = this.state;
        if (!attachmentText) {
            return null;
        }
        const spans = ansicolor_1.default
            .parse(attachmentText)
            .spans.map(({ color, bgColor, text }, idx) => {
            const style = {};
            if (color) {
                if (color.name) {
                    style.color =
                        COLORS[color.name + (color.dim ? 'Dim' : '')] || COLORS[color.name] || '';
                }
                if (color.bright) {
                    style.fontWeight = 500;
                }
            }
            if (bgColor && bgColor.name) {
                style.background =
                    COLORS[bgColor.name + (bgColor.dim ? 'Dim' : '')] ||
                        COLORS[bgColor.name] ||
                        '';
            }
            return (<span style={style} key={idx}>
            {text}
          </span>);
        });
        return (<previewPanelItem_1.default>
        <CodeWrapper>{spans}</CodeWrapper>
      </previewPanelItem_1.default>);
    }
}
exports.default = LogFileViewer;
const CodeWrapper = (0, styled_1.default)('pre') `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  width: 100%;
  margin-bottom: 0;
  &:after {
    content: '';
  }
`;
//# sourceMappingURL=logFileViewer.jsx.map