Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const TeamActions = reflux_1.default.createActions([
    'createTeam',
    'createTeamError',
    'createTeamSuccess',
    'fetchAll',
    'fetchAllError',
    'fetchAllSuccess',
    'fetchDetails',
    'fetchDetailsError',
    'fetchDetailsSuccess',
    'loadTeams',
    'loadUserTeams',
    'removeTeam',
    'removeTeamError',
    'removeTeamSuccess',
    'update',
    'updateError',
    'updateSuccess',
]);
exports.default = TeamActions;
//# sourceMappingURL=teamActions.jsx.map