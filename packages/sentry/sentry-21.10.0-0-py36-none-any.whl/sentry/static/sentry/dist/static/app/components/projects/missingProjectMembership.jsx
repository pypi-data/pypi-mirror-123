Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const teams_1 = require("app/actionCreators/teams");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
class MissingProjectMembership extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: false,
            error: false,
            project: this.props.project,
            team: '',
        };
        this.getPendingTeamOption = (team) => {
            return {
                value: team,
                label: <DisabledLabel>{(0, locale_1.t)(`#${team}`)}</DisabledLabel>,
            };
        };
    }
    joinTeam(teamSlug) {
        this.setState({
            loading: true,
        });
        (0, teams_1.joinTeam)(this.props.api, {
            orgId: this.props.organization.slug,
            teamId: teamSlug,
        }, {
            success: () => {
                this.setState({
                    loading: false,
                    error: false,
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Request to join team sent.'));
            },
            error: () => {
                this.setState({
                    loading: false,
                    error: true,
                });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('There was an error while trying to request access.'));
            },
        });
    }
    renderJoinTeam(teamSlug, features) {
        const team = teamStore_1.default.getBySlug(teamSlug);
        if (!team) {
            return null;
        }
        if (this.state.loading) {
            if (features.has('open-membership')) {
                return <button_1.default busy>{(0, locale_1.t)('Join Team')}</button_1.default>;
            }
            return <button_1.default busy>{(0, locale_1.t)('Request Access')}</button_1.default>;
        }
        else if (team === null || team === void 0 ? void 0 : team.isPending) {
            return <button_1.default disabled>{(0, locale_1.t)('Request Pending')}</button_1.default>;
        }
        else if (features.has('open-membership')) {
            return (<button_1.default priority="primary" type="button" onClick={this.joinTeam.bind(this, teamSlug)}>
          {(0, locale_1.t)('Join Team')}
        </button_1.default>);
        }
        return (<button_1.default priority="primary" type="button" onClick={this.joinTeam.bind(this, teamSlug)}>
        {(0, locale_1.t)('Request Access')}
      </button_1.default>);
    }
    getTeamsForAccess() {
        var _a, _b;
        const request = [];
        const pending = [];
        const teams = (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.teams) !== null && _b !== void 0 ? _b : [];
        teams.forEach(({ slug }) => {
            const team = teamStore_1.default.getBySlug(slug);
            if (!team) {
                return;
            }
            team.isPending ? pending.push(team.slug) : request.push(team.slug);
        });
        return [request, pending];
    }
    render() {
        var _a, _b;
        const { organization } = this.props;
        const teamSlug = this.state.team;
        const teams = (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.teams) !== null && _b !== void 0 ? _b : [];
        const features = new Set(organization.features);
        const teamAccess = [
            {
                label: (0, locale_1.t)('Request Access'),
                options: this.getTeamsForAccess()[0].map(request => ({
                    value: request,
                    label: (0, locale_1.t)(`#${request}`),
                })),
            },
            {
                label: (0, locale_1.t)('Pending Requests'),
                options: this.getTeamsForAccess()[1].map(pending => this.getPendingTeamOption(pending)),
            },
        ];
        return (<StyledPanel>
        {!teams.length ? (<emptyMessage_1.default icon={<icons_1.IconFlag size="xl"/>}>
            {(0, locale_1.t)('No teams have access to this project yet. Ask an admin to add your team to this project.')}
          </emptyMessage_1.default>) : (<emptyMessage_1.default icon={<icons_1.IconFlag size="xl"/>} title={(0, locale_1.t)("You're not a member of this project.")} description={(0, locale_1.t)(`You'll need to join a team with access before you can view this data.`)} action={<Field>
                <StyledSelectControl name="select" placeholder={(0, locale_1.t)('Select a Team')} options={teamAccess} onChange={teamObj => {
                        const team = teamObj ? teamObj.value : null;
                        this.setState({ team });
                    }}/>
                {teamSlug ? (this.renderJoinTeam(teamSlug, features)) : (<button_1.default disabled>{(0, locale_1.t)('Select a Team')}</button_1.default>)}
              </Field>}/>)}
      </StyledPanel>);
    }
}
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  margin: ${(0, space_1.default)(2)} 0;
`;
const Field = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  gap: ${(0, space_1.default)(2)};
  text-align: left;
`;
const StyledSelectControl = (0, styled_1.default)(selectControl_1.default) `
  width: 250px;
`;
const DisabledLabel = (0, styled_1.default)('div') `
  display: flex;
  opacity: 0.5;
  overflow: hidden;
`;
exports.default = (0, withApi_1.default)(MissingProjectMembership);
//# sourceMappingURL=missingProjectMembership.jsx.map