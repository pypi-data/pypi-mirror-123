Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const locale_1 = require("../../locale");
const externalLink_1 = (0, tslib_1.__importDefault)(require("../links/externalLink"));
const SidebarPanelItem = ({ hasSeen, title, image, message, link, cta, children, }) => (<SidebarPanelItemRoot>
    {title && <Title hasSeen={hasSeen}>{title}</Title>}
    {image && (<ImageBox>
        <img src={image}/>
      </ImageBox>)}
    {message && <Message>{message}</Message>}

    {children}

    {link && (<Text>
        <externalLink_1.default href={link}>{cta || (0, locale_1.t)('Read More')}</externalLink_1.default>
      </Text>)}
  </SidebarPanelItemRoot>);
exports.default = SidebarPanelItem;
const SidebarPanelItemRoot = (0, styled_1.default)('div') `
  line-height: 1.5;
  border-top: 1px solid ${p => p.theme.innerBorder};
  background: ${p => p.theme.background};
  font-size: ${p => p.theme.fontSizeMedium};
  padding: ${(0, space_1.default)(3)};
`;
const ImageBox = (0, styled_1.default)('div') `
  border: 1px solid #e1e4e5;
  padding: ${(0, space_1.default)(2)};
  border-radius: 2px;
`;
const Title = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeLarge};
  margin-bottom: ${(0, space_1.default)(1)};
  color: ${p => p.theme.textColor};
  ${p => !p.hasSeen && 'font-weight: 600;'};

  .culprit {
    font-weight: normal;
  }
`;
const Text = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(0.5)};

  &:last-child {
    margin-bottom: 0;
  }
`;
const Message = (0, styled_1.default)(Text) `
  color: ${p => p.theme.subText};
`;
//# sourceMappingURL=sidebarPanelItem.jsx.map