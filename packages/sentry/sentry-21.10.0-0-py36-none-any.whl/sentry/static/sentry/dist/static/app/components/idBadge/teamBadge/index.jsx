Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const badge_1 = (0, tslib_1.__importDefault)(require("./badge"));
class TeamBadgeContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.state = { team: this.props.team };
        this.unlistener = teamStore_1.default.listen((team) => this.onTeamStoreUpdate(team), undefined);
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        if (this.state.team === nextProps.team) {
            return;
        }
        if ((0, isEqual_1.default)(this.state.team, nextProps.team)) {
            return;
        }
        this.setState({ team: nextProps.team });
    }
    componentWillUnmount() {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    }
    onTeamStoreUpdate(updatedTeam) {
        if (!updatedTeam.has(this.state.team.id)) {
            return;
        }
        const team = teamStore_1.default.getById(this.state.team.id);
        if (!team || (0, isEqual_1.default)(team.avatar, this.state.team.avatar)) {
            return;
        }
        this.setState({ team });
    }
    render() {
        return <badge_1.default {...this.props} team={this.state.team}/>;
    }
}
exports.default = TeamBadgeContainer;
//# sourceMappingURL=index.jsx.map