Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const makeKey = (prefix) => `${prefix}-banner-dismissed`;
function dismissBanner(bannerKey) {
    localStorage.setItem(makeKey(bannerKey), 'true');
}
function useDismissable(bannerKey) {
    const key = makeKey(bannerKey);
    const [value, setValue] = React.useState(localStorage.getItem(key));
    const dismiss = () => {
        setValue('true');
        dismissBanner(bannerKey);
    };
    return [value === 'true', dismiss];
}
const Banner = ({ title, subtitle, isDismissable = true, dismissKey = 'generic-banner', className, backgroundImg, backgroundComponent, children, }) => {
    const [dismissed, dismiss] = useDismissable(dismissKey);
    if (dismissed) {
        return null;
    }
    return (<BannerWrapper backgroundImg={backgroundImg} className={className}>
      {backgroundComponent}
      {isDismissable ? <CloseButton onClick={dismiss} aria-label={(0, locale_1.t)('Close')}/> : null}
      <BannerContent>
        <BannerTitle>{title}</BannerTitle>
        <BannerSubtitle>{subtitle}</BannerSubtitle>
        <StyledButtonBar gap={1}>{children}</StyledButtonBar>
      </BannerContent>
    </BannerWrapper>);
};
Banner.dismiss = dismissBanner;
const BannerWrapper = (0, styled_1.default)('div') `
  ${p => p.backgroundImg
    ? (0, react_1.css) `
          background: url(${p.backgroundImg});
          background-repeat: no-repeat;
          background-size: cover;
          background-position: center center;
        `
    : (0, react_1.css) `
          background-color: ${p.theme.gray500};
        `}
  display: flex;
  overflow: hidden;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-bottom: ${(0, space_1.default)(2)};
  box-shadow: ${p => p.theme.dropShadowLight};
  border-radius: ${p => p.theme.borderRadius};
  height: 180px;
  color: ${p => p.theme.white};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    height: 220px;
  }
`;
const BannerContent = (0, styled_1.default)('div') `
  position: absolute;
  display: grid;
  justify-items: center;
  grid-template-rows: repeat(3, max-content);
  text-align: center;
  padding: ${(0, space_1.default)(4)};
`;
const BannerTitle = (0, styled_1.default)('h1') `
  margin: 0;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    font-size: 40px;
  }
`;
const BannerSubtitle = (0, styled_1.default)('div') `
  margin: 0;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    font-size: ${p => p.theme.fontSizeExtraLarge};
  }
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  margin-top: ${(0, space_1.default)(2)};
  width: fit-content;
`;
const CloseButton = (0, styled_1.default)(button_1.default) `
  position: absolute;
  display: block;
  top: ${(0, space_1.default)(2)};
  right: ${(0, space_1.default)(2)};
  color: ${p => p.theme.white};
  cursor: pointer;
  z-index: 1;
`;
CloseButton.defaultProps = {
    icon: <icons_1.IconClose />,
    label: (0, locale_1.t)('Close'),
    priority: 'link',
    borderless: true,
    size: 'xsmall',
};
exports.default = Banner;
//# sourceMappingURL=banner.jsx.map