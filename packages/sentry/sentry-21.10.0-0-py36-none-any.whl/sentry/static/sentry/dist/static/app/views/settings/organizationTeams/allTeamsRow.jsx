Object.defineProperty(exports, "__esModule", { value: true });
exports.AllTeamsRow = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const teams_1 = require("app/actionCreators/teams");
const teamActions_1 = (0, tslib_1.__importDefault)(require("app/actions/teamActions"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class AllTeamsRow extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
            error: false,
        };
        this.handleRequestAccess = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { team } = this.props;
            try {
                this.joinTeam({
                    successMessage: (0, locale_1.tct)('You have requested access to [team]', {
                        team: `#${team.slug}`,
                    }),
                    errorMessage: (0, locale_1.tct)('Unable to request access to [team]', {
                        team: `#${team.slug}`,
                    }),
                });
                // Update team so that `isPending` is true
                teamActions_1.default.updateSuccess(team.slug, Object.assign(Object.assign({}, team), { isPending: true }));
            }
            catch (_err) {
                // No need to do anything
            }
        });
        this.handleJoinTeam = () => {
            const { team } = this.props;
            this.joinTeam({
                successMessage: (0, locale_1.tct)('You have joined [team]', {
                    team: `#${team.slug}`,
                }),
                errorMessage: (0, locale_1.tct)('Unable to join [team]', {
                    team: `#${team.slug}`,
                }),
            });
        };
        this.joinTeam = ({ successMessage, errorMessage, }) => {
            const { api, organization, team } = this.props;
            this.setState({
                loading: true,
            });
            return new Promise((resolve, reject) => (0, teams_1.joinTeam)(api, {
                orgId: organization.slug,
                teamId: team.slug,
            }, {
                success: () => {
                    this.setState({
                        loading: false,
                        error: false,
                    });
                    (0, indicator_1.addSuccessMessage)(successMessage);
                    resolve();
                },
                error: () => {
                    this.setState({
                        loading: false,
                        error: true,
                    });
                    (0, indicator_1.addErrorMessage)(errorMessage);
                    reject(new Error('Unable to join team'));
                },
            }));
        };
        this.handleLeaveTeam = () => {
            const { api, organization, team } = this.props;
            this.setState({
                loading: true,
            });
            (0, teams_1.leaveTeam)(api, {
                orgId: organization.slug,
                teamId: team.slug,
            }, {
                success: () => {
                    this.setState({
                        loading: false,
                        error: false,
                    });
                    (0, indicator_1.addSuccessMessage)((0, locale_1.tct)('You have left [team]', {
                        team: `#${team.slug}`,
                    }));
                },
                error: () => {
                    this.setState({
                        loading: false,
                        error: true,
                    });
                    (0, indicator_1.addErrorMessage)((0, locale_1.tct)('Unable to leave [team]', {
                        team: `#${team.slug}`,
                    }));
                },
            });
        };
    }
    render() {
        const { team, urlPrefix, openMembership } = this.props;
        const display = (<idBadge_1.default team={team} avatarSize={36} description={(0, locale_1.tn)('%s Member', '%s Members', team.memberCount)}/>);
        // You can only view team details if you have access to team -- this should account
        // for your role + org open membership
        const canViewTeam = team.hasAccess;
        return (<TeamPanelItem>
        <TeamNameWrapper>
          {canViewTeam ? (<TeamLink to={`${urlPrefix}teams/${team.slug}/`}>{display}</TeamLink>) : (display)}
        </TeamNameWrapper>
        <Spacer>
          {this.state.loading ? (<button_1.default size="small" disabled>
              ...
            </button_1.default>) : team.isMember ? (<button_1.default size="small" onClick={this.handleLeaveTeam}>
              {(0, locale_1.t)('Leave Team')}
            </button_1.default>) : team.isPending ? (<button_1.default size="small" disabled title={(0, locale_1.t)('Your request to join this team is being reviewed by organization owners')}>
              {(0, locale_1.t)('Request Pending')}
            </button_1.default>) : openMembership ? (<button_1.default size="small" onClick={this.handleJoinTeam}>
              {(0, locale_1.t)('Join Team')}
            </button_1.default>) : (<button_1.default size="small" onClick={this.handleRequestAccess}>
              {(0, locale_1.t)('Request Access')}
            </button_1.default>)}
        </Spacer>
      </TeamPanelItem>);
    }
}
exports.AllTeamsRow = AllTeamsRow;
const TeamLink = (0, styled_1.default)(link_1.default) `
  display: inline-block;

  &.focus-visible {
    margin: -${(0, space_1.default)(1)};
    padding: ${(0, space_1.default)(1)};
    background: #f2eff5;
    border-radius: 3px;
    outline: none;
  }
`;
exports.default = (0, withApi_1.default)(AllTeamsRow);
const TeamPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  padding: 0;
  align-items: center;
`;
const Spacer = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
`;
const TeamNameWrapper = (0, styled_1.default)(Spacer) `
  flex: 1;
`;
//# sourceMappingURL=allTeamsRow.jsx.map