Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const userMisery_1 = (0, tslib_1.__importDefault)(require("app/components/userMisery"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
const queryString_1 = require("app/utils/queryString");
const data_1 = require("app/views/performance/data");
const utils_1 = require("app/views/performance/transactionSummary/transactionVitals/utils");
const utils_2 = require("app/views/performance/transactionSummary/utils");
const vitalInfo_1 = (0, tslib_1.__importDefault)(require("app/views/performance/vitalDetail/vitalInfo"));
function UserStats({ isLoading, hasWebVitals, error, totals, location, organization, transactionName, }) {
    let userMisery = error !== null ? <div>{'\u2014'}</div> : <placeholder_1.default height="34px"/>;
    if (!isLoading && error === null && totals) {
        const threshold = totals.project_threshold_config[1];
        const miserableUsers = totals.count_miserable_user;
        const userMiseryScore = totals.user_misery;
        const totalUsers = totals.count_unique_user;
        userMisery = (<userMisery_1.default bars={40} barHeight={30} userMisery={userMiseryScore} miseryLimit={threshold} totalUsers={totalUsers} miserableUsers={miserableUsers}/>);
    }
    const webVitalsTarget = (0, utils_1.vitalsRouteWithQuery)({
        orgSlug: organization.slug,
        transaction: transactionName,
        projectID: (0, queryString_1.decodeScalar)(location.query.project),
        query: location.query,
    });
    return (<react_1.Fragment>
      {hasWebVitals && (<react_1.Fragment>
          <VitalsHeading>
            <styles_1.SectionHeading>
              {(0, locale_1.t)('Web Vitals')}
              <questionTooltip_1.default position="top" title={(0, locale_1.t)('Web Vitals with p75 better than the "poor" threshold, as defined by Google Web Vitals.')} size="sm"/>
            </styles_1.SectionHeading>
            <link_1.default to={webVitalsTarget}>
              <icons_1.IconOpen />
            </link_1.default>
          </VitalsHeading>
          <vitalInfo_1.default location={location} vital={[fields_1.WebVital.FCP, fields_1.WebVital.LCP, fields_1.WebVital.FID, fields_1.WebVital.CLS]} hideVitalPercentNames hideDurationDetail/>
          <utils_2.SidebarSpacer />
        </react_1.Fragment>)}
      <styles_1.SectionHeading>
        {(0, locale_1.t)('User Misery')}
        <questionTooltip_1.default position="top" title={(0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.USER_MISERY_NEW)} size="sm"/>
      </styles_1.SectionHeading>
      {userMisery}
      <utils_2.SidebarSpacer />
    </react_1.Fragment>);
}
const VitalsHeading = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
`;
exports.default = UserStats;
//# sourceMappingURL=userStats.jsx.map