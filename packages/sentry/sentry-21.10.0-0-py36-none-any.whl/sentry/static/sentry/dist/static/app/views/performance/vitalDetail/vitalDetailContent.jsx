Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const createAlertButton_1 = require("app/components/createAlertButton");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const TeamKeyTransactionManager = (0, tslib_1.__importStar)(require("app/components/performance/teamKeyTransactionsManager"));
const icons_1 = require("app/icons");
const iconFlag_1 = require("app/icons/iconFlag");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const fields_1 = require("app/utils/discover/fields");
const isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
const queryString_1 = require("app/utils/queryString");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const breadcrumb_1 = (0, tslib_1.__importDefault)(require("../breadcrumb"));
const utils_2 = require("../utils");
const table_1 = (0, tslib_1.__importDefault)(require("./table"));
const utils_3 = require("./utils");
const vitalChart_1 = (0, tslib_1.__importDefault)(require("./vitalChart"));
const vitalInfo_1 = (0, tslib_1.__importDefault)(require("./vitalInfo"));
const FRONTEND_VITALS = [fields_1.WebVital.FCP, fields_1.WebVital.LCP, fields_1.WebVital.FID, fields_1.WebVital.CLS];
function getSummaryConditions(query) {
    const parsed = new tokenizeSearch_1.MutableSearch(query);
    parsed.freeText = [];
    return parsed.formatString();
}
class VitalDetailContent extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            incompatibleAlertNotice: null,
            error: undefined,
        };
        this.handleSearch = (query) => {
            const { location } = this.props;
            const queryParams = (0, getParams_1.getParams)(Object.assign(Object.assign({}, (location.query || {})), { query }));
            // do not propagate pagination when making a new search
            const searchQueryParams = (0, omit_1.default)(queryParams, 'cursor');
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        this.generateTagUrl = (key, value) => {
            const { location } = this.props;
            const query = (0, utils_1.generateQueryWithTag)(location.query, { key, value });
            return Object.assign(Object.assign({}, location), { query });
        };
        this.handleIncompatibleQuery = (incompatibleAlertNoticeFn, _errors) => {
            const incompatibleAlertNotice = incompatibleAlertNoticeFn(() => this.setState({ incompatibleAlertNotice: null }));
            this.setState({ incompatibleAlertNotice });
        };
        this.setError = (error) => {
            this.setState({ error });
        };
    }
    renderCreateAlertButton() {
        const { eventView, organization, projects } = this.props;
        return (<createAlertButton_1.CreateAlertFromViewButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={this.handleIncompatibleQuery} onSuccess={() => { }} referrer="performance"/>);
    }
    renderVitalSwitcher() {
        const { vitalName, location } = this.props;
        const position = FRONTEND_VITALS.indexOf(vitalName);
        if (position < 0) {
            return null;
        }
        const previousDisabled = position === 0;
        const nextDisabled = position === FRONTEND_VITALS.length - 1;
        const switchVital = newVitalName => {
            return () => {
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: Object.assign(Object.assign({}, location.query), { vitalName: newVitalName }),
                });
            };
        };
        return (<buttonBar_1.default merged>
        <button_1.default icon={<icons_1.IconChevron direction="left" size="sm"/>} aria-label={(0, locale_1.t)('Previous')} disabled={previousDisabled} onClick={switchVital(FRONTEND_VITALS[position - 1])}/>
        <button_1.default icon={<icons_1.IconChevron direction="right" size="sm"/>} aria-label={(0, locale_1.t)('Next')} disabled={nextDisabled} onClick={switchVital(FRONTEND_VITALS[position + 1])}/>
      </buttonBar_1.default>);
    }
    renderError() {
        const { error } = this.state;
        if (!error) {
            return null;
        }
        return (<alert_1.default type="error" icon={<iconFlag_1.IconFlag size="md"/>}>
        {error}
      </alert_1.default>);
    }
    render() {
        const { location, eventView, organization, vitalName, projects, teams } = this.props;
        const { incompatibleAlertNotice } = this.state;
        const query = (0, queryString_1.decodeScalar)(location.query.query, '');
        const vital = vitalName || fields_1.WebVital.LCP;
        const filterString = (0, utils_2.getTransactionSearchQuery)(location);
        const summaryConditions = getSummaryConditions(filterString);
        const description = utils_3.vitalDescription[vitalName];
        const isSuperuser = (0, isActiveSuperuser_1.isActiveSuperuser)();
        const userTeams = teams.filter(({ isMember }) => isMember || isSuperuser);
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumb_1.default organization={organization} location={location} vitalName={vital}/>
            <Layout.Title>{utils_3.vitalMap[vital]}</Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <buttonBar_1.default gap={1}>
              <feature_1.default organization={organization} features={['incidents']}>
                {({ hasFeature }) => hasFeature && this.renderCreateAlertButton()}
              </feature_1.default>
              {this.renderVitalSwitcher()}
            </buttonBar_1.default>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          {this.renderError()}
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main fullWidth>
            <StyledDescription>{description}</StyledDescription>
            <StyledSearchBar searchSource="performance_vitals" organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch}/>
            <vitalChart_1.default organization={organization} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>
            <StyledVitalInfo>
              <vitalInfo_1.default location={location} vital={vital}/>
            </StyledVitalInfo>
            <TeamKeyTransactionManager.Provider organization={organization} teams={userTeams} selectedTeams={['myteams']} selectedProjects={eventView.project.map(String)}>
              <table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={this.setError} summaryConditions={summaryConditions}/>
            </TeamKeyTransactionManager.Provider>
          </Layout.Main>
        </Layout.Body>
      </React.Fragment>);
    }
}
const StyledDescription = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin-bottom: ${(0, space_1.default)(3)};
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  margin-bottom: ${(0, space_1.default)(2)};
`;
const StyledVitalInfo = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(3)};
`;
exports.default = (0, withTeams_1.default)((0, withProjects_1.default)(VitalDetailContent));
//# sourceMappingURL=vitalDetailContent.jsx.map