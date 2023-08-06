Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const ResourceCard = ({ title, link, imgUrl }) => (<ResourceCardWrapper onClick={() => (0, analytics_1.analytics)('orgdash.resource_clicked', { link, title })}>
    <StyledLink href={link}>
      <StyledImg src={imgUrl} alt={title}/>
      <StyledTitle>{title}</StyledTitle>
    </StyledLink>
  </ResourceCardWrapper>);
exports.default = ResourceCard;
const ResourceCardWrapper = (0, styled_1.default)(panels_1.Panel) `
  display: flex;
  flex: 1;
  align-items: center;
  padding: ${(0, space_1.default)(3)};
  margin-bottom: 0;
`;
const StyledLink = (0, styled_1.default)(externalLink_1.default) `
  flex: 1;
`;
const StyledImg = (0, styled_1.default)('img') `
  display: block;
  margin: 0 auto ${(0, space_1.default)(3)} auto;
  height: 160px;
`;
const StyledTitle = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.fontSizeLarge};
  text-align: center;
  font-weight: bold;
`;
//# sourceMappingURL=resourceCard.jsx.map