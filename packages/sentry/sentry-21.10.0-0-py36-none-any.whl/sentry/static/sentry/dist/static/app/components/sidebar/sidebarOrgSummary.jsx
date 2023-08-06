Object.defineProperty(exports, "__esModule", { value: true });
exports.OrgSummary = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const organizationAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/organizationAvatar"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const SidebarOrgSummary = ({ organization, projectCount }) => (<OrgSummary>
    <organizationAvatar_1.default organization={organization} size={36}/>
    <Details>
      <Name>{organization.name}</Name>
      {!!projectCount && <Extra>{(0, locale_1.tn)('%s project', '%s projects', projectCount)}</Extra>}
    </Details>
  </OrgSummary>);
const OrgSummary = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  padding: ${(0, space_1.default)(1)} ${p => p.theme.sidebar.menuSpacing};
  overflow: hidden;
`;
exports.OrgSummary = OrgSummary;
const Details = (0, styled_1.default)('div') `
  overflow: hidden;
`;
const Name = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.fontSizeLarge};
  line-height: 1.1;
  font-weight: bold;
  ${overflowEllipsis_1.default};
`;
const Extra = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  line-height: 1;
  margin-top: ${(0, space_1.default)(0.5)};
  ${overflowEllipsis_1.default};
`;
exports.default = SidebarOrgSummary;
//# sourceMappingURL=sidebarOrgSummary.jsx.map