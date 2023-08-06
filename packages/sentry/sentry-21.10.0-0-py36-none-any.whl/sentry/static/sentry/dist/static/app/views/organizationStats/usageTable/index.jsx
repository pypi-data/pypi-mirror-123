Object.defineProperty(exports, "__esModule", { value: true });
exports.CellProject = exports.CellStat = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const headerItem_1 = require("app/components/organizations/headerItem");
const panels_1 = require("app/components/panels");
const panelTable_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelTable"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const utils_1 = require("../utils");
const DOCS_URL = 'https://docs.sentry.io/product/accounts/membership/#restricting-access';
class UsageTable extends React.Component {
    constructor() {
        super(...arguments);
        this.getErrorMessage = errorMessage => {
            if (errorMessage.projectStats.responseJSON.detail === 'No projects available') {
                return (<emptyMessage_1.default icon={<icons_1.IconWarning color="gray300" size="48"/>} title={(0, locale_1.t)("You don't have access to any projects, or your organization has no projects.")} description={(0, locale_1.tct)('Learn more about [link:Project Access]', {
                        link: <externalLink_1.default href={DOCS_URL}/>,
                    })}/>);
            }
            return <icons_1.IconWarning color="gray300" size="48"/>;
        };
    }
    get formatUsageOptions() {
        const { dataCategory } = this.props;
        return {
            isAbbreviated: dataCategory !== types_1.DataCategory.ATTACHMENTS,
            useUnitScaling: dataCategory === types_1.DataCategory.ATTACHMENTS,
        };
    }
    renderTableRow(stat) {
        const { dataCategory } = this.props;
        const { project, total, accepted, filtered, dropped } = stat;
        return [
            <exports.CellProject key={0}>
        <link_1.default to={stat.projectLink}>
          <StyledIdBadge avatarSize={16} disableLink hideOverflow project={project} displayName={project.slug}/>
        </link_1.default>
        <headerItem_1.SettingsIconLink to={stat.projectSettingsLink}>
          <icons_1.IconSettings size={theme_1.default.iconSizes.sm}/>
        </headerItem_1.SettingsIconLink>
      </exports.CellProject>,
            <exports.CellStat key={1}>
        {(0, utils_1.formatUsageWithUnits)(total, dataCategory, this.formatUsageOptions)}
      </exports.CellStat>,
            <exports.CellStat key={2}>
        {(0, utils_1.formatUsageWithUnits)(accepted, dataCategory, this.formatUsageOptions)}
      </exports.CellStat>,
            <exports.CellStat key={3}>
        {(0, utils_1.formatUsageWithUnits)(filtered, dataCategory, this.formatUsageOptions)}
      </exports.CellStat>,
            <exports.CellStat key={4}>
        {(0, utils_1.formatUsageWithUnits)(dropped, dataCategory, this.formatUsageOptions)}
      </exports.CellStat>,
        ];
    }
    render() {
        const { isEmpty, isLoading, isError, errors, headers, usageStats } = this.props;
        if (isError) {
            return (<panels_1.Panel>
          <errorPanel_1.default height="256px">{this.getErrorMessage(errors)}</errorPanel_1.default>
        </panels_1.Panel>);
        }
        return (<StyledPanelTable isLoading={isLoading} isEmpty={isEmpty} headers={headers}>
        {usageStats.map(s => this.renderTableRow(s))}
      </StyledPanelTable>);
    }
}
exports.default = UsageTable;
const StyledPanelTable = (0, styled_1.default)(panelTable_1.default) `
  grid-template-columns: repeat(5, auto);

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 1fr repeat(4, minmax(0, auto));
  }
`;
exports.CellStat = (0, styled_1.default)('div') `
  flex-shrink: 1;
  text-align: right;
  font-variant-numeric: tabular-nums;
`;
exports.CellProject = (0, styled_1.default)(exports.CellStat) `
  display: flex;
  align-items: center;
  text-align: left;
`;
const StyledIdBadge = (0, styled_1.default)(idBadge_1.default) `
  overflow: hidden;
  white-space: nowrap;
  flex-shrink: 1;
`;
//# sourceMappingURL=index.jsx.map