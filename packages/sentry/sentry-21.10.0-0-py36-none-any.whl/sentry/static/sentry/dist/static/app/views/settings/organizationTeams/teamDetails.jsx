Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const indicator_1 = require("app/actionCreators/indicator");
const teams_1 = require("app/actionCreators/teams");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const listLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/listLink"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
class TeamDetails extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.handleRequestAccess = () => {
            const { api, params } = this.props;
            const { team } = this.state;
            if (!team) {
                return;
            }
            this.setState({
                requesting: true,
            });
            (0, teams_1.joinTeam)(api, {
                orgId: params.orgId,
                teamId: team.slug,
            }, {
                success: () => {
                    (0, indicator_1.addSuccessMessage)((0, locale_1.tct)('You have requested access to [team]', {
                        team: `#${team.slug}`,
                    }));
                    this.setState({
                        requesting: false,
                    });
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)((0, locale_1.tct)('Unable to request access to [team]', {
                        team: `#${team.slug}`,
                    }));
                    this.setState({
                        requesting: false,
                    });
                },
            });
        };
        this.fetchData = () => {
            this.setState({
                loading: true,
                error: false,
            });
            (0, teams_1.fetchTeamDetails)(this.props.api, this.props.params);
        };
        this.onTeamChange = (data) => {
            const team = this.state.team;
            if (data.slug !== (team === null || team === void 0 ? void 0 : team.slug)) {
                const orgId = this.props.params.orgId;
                react_router_1.browserHistory.replace(`/organizations/${orgId}/teams/${data.slug}/settings/`);
            }
            else {
                this.setState({
                    team: Object.assign(Object.assign({}, team), data),
                });
            }
        };
    }
    getInitialState() {
        const team = teamStore_1.default.getBySlug(this.props.params.teamId);
        return {
            loading: !teamStore_1.default.initialized,
            error: false,
            requesting: false,
            team,
        };
    }
    componentDidUpdate(prevProps) {
        const { params } = this.props;
        if (prevProps.params.teamId !== params.teamId ||
            prevProps.params.orgId !== params.orgId) {
            this.fetchData();
        }
        if (!(0, isEqual_1.default)(this.props.teams, prevProps.teams)) {
            this.setActiveTeam();
        }
    }
    setActiveTeam() {
        const team = teamStore_1.default.getBySlug(this.props.params.teamId);
        const loading = !teamStore_1.default.initialized;
        const error = !loading && !team;
        this.setState({ team, loading, error });
    }
    render() {
        const { children, params, routes } = this.props;
        const { team, loading, requesting, error } = this.state;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (!team || !team.hasAccess) {
            return (<alert_1.default type="warning">
          {team ? (<RequestAccessWrapper>
              {(0, locale_1.tct)('You do not have access to the [teamSlug] team.', {
                        teamSlug: <strong>{`#${team.slug}`}</strong>,
                    })}
              <button_1.default disabled={requesting || team.isPending} size="small" onClick={this.handleRequestAccess}>
                {team.isPending ? (0, locale_1.t)('Request Pending') : (0, locale_1.t)('Request Access')}
              </button_1.default>
            </RequestAccessWrapper>) : (<div>{(0, locale_1.t)('You do not have access to this team.')}</div>)}
        </alert_1.default>);
        }
        if (error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        // `/organizations/${orgId}/teams/${teamId}`;
        const routePrefix = (0, recreateRoute_1.default)('', { routes, params, stepBack: -1 });
        const navigationTabs = [
            <listLink_1.default key={0} to={`${routePrefix}members/`}>
        {(0, locale_1.t)('Members')}
      </listLink_1.default>,
            <listLink_1.default key={1} to={`${routePrefix}projects/`}>
        {(0, locale_1.t)('Projects')}
      </listLink_1.default>,
            <listLink_1.default key={2} to={`${routePrefix}notifications/`}>
        {(0, locale_1.t)('Notifications')}
      </listLink_1.default>,
            <listLink_1.default key={3} to={`${routePrefix}settings/`}>
        {(0, locale_1.t)('Settings')}
      </listLink_1.default>,
        ];
        return (<div>
        <sentryDocumentTitle_1.default title={(0, locale_1.t)('Team Details')} orgSlug={params.orgId}/>
        <h3>
          <idBadge_1.default hideAvatar team={team} avatarSize={36}/>
        </h3>

        <navTabs_1.default underlined>{navigationTabs}</navTabs_1.default>

        {React.isValidElement(children) &&
                React.cloneElement(children, {
                    team,
                    onTeamChange: this.onTeamChange,
                })}
      </div>);
    }
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withTeams_1.default)(TeamDetails)));
const RequestAccessWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
`;
//# sourceMappingURL=teamDetails.jsx.map