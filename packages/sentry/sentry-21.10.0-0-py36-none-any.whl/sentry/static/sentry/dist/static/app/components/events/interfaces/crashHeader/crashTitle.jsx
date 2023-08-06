Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const CrashTitle = ({ title, newestFirst, beforeTitle, hideGuide = false, onChange, }) => {
    const handleToggleOrder = () => {
        if (onChange) {
            onChange({ newestFirst: !newestFirst });
        }
    };
    return (<Wrapper>
      {beforeTitle}
      <StyledH3>
        <guideAnchor_1.default target="exception" disabled={hideGuide} position="bottom">
          {title}
        </guideAnchor_1.default>
        {onChange && (<tooltip_1.default title={(0, locale_1.t)('Toggle stack trace order')}>
            <small>
              (
              <span onClick={handleToggleOrder}>
                {newestFirst ? (0, locale_1.t)('most recent call first') : (0, locale_1.t)('most recent call last')}
              </span>
              )
            </small>
          </tooltip_1.default>)}
      </StyledH3>
    </Wrapper>);
};
exports.default = CrashTitle;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  flex-grow: 1;
  justify-content: flex-start;
`;
const StyledH3 = (0, styled_1.default)('h3') `
  margin-bottom: 0;
  max-width: 100%;
  white-space: nowrap;
`;
//# sourceMappingURL=crashTitle.jsx.map