Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("../../utils");
function DetailsHeader({ hasIncidentRuleDetailsError, rule, params }) {
    var _a;
    const isRuleReady = !!rule && !hasIncidentRuleDetailsError;
    const project = (_a = rule === null || rule === void 0 ? void 0 : rule.projects) === null || _a === void 0 ? void 0 : _a[0];
    const settingsLink = rule &&
        `/organizations/${params.orgId}/alerts/${(0, utils_1.isIssueAlert)(rule) ? 'rules' : 'metric-rules'}/${project}/${rule.id}/`;
    return (<Header>
      <BreadCrumbBar>
        <AlertBreadcrumbs crumbs={[
            { label: (0, locale_1.t)('Alerts'), to: `/organizations/${params.orgId}/alerts/rules/` },
            { label: (0, locale_1.t)('Alert Rule') },
        ]}/>
        <Controls>
          <button_1.default icon={<icons_1.IconEdit />} to={settingsLink}>
            {(0, locale_1.t)('Edit Rule')}
          </button_1.default>
        </Controls>
      </BreadCrumbBar>
      <Details>
        <RuleTitle data-test-id="incident-rule-title" loading={!isRuleReady}>
          {rule && !hasIncidentRuleDetailsError ? rule.name : (0, locale_1.t)('Loading')}
        </RuleTitle>
      </Details>
    </Header>);
}
exports.default = DetailsHeader;
const Header = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.backgroundSecondary};
  border-bottom: 1px solid ${p => p.theme.border};
`;
const BreadCrumbBar = (0, styled_1.default)('div') `
  display: flex;
  margin-bottom: 0;
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(4)} ${(0, space_1.default)(1)};
`;
const AlertBreadcrumbs = (0, styled_1.default)(breadcrumbs_1.default) `
  flex-grow: 1;
  font-size: ${p => p.theme.fontSizeExtraLarge};
  padding: 0;
`;
const Controls = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
`;
const Details = (0, styled_1.default)(organization_1.PageHeader) `
  margin-bottom: 0;
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(4)} ${(0, space_1.default)(2)};

  grid-template-columns: max-content auto;
  display: grid;
  grid-gap: ${(0, space_1.default)(3)};
  grid-auto-flow: column;

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: auto;
    grid-auto-flow: row;
  }
`;
const RuleTitle = (0, styled_1.default)(pageHeading_1.default, {
    shouldForwardProp: p => typeof p === 'string' && (0, is_prop_valid_1.default)(p) && p !== 'loading',
}) `
  ${p => p.loading && 'opacity: 0'};
  line-height: 1.5;
`;
//# sourceMappingURL=header.jsx.map