Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
const useTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/useTeams"));
/**
 * Higher order component that provides a list of teams
 */
const withTeams = (WrappedComponent) => {
    const WithTeams = props => {
        const { teams } = (0, useTeams_1.default)();
        return <WrappedComponent teams={teams} {...props}/>;
    };
    WithTeams.displayName = `withTeams(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithTeams;
};
exports.default = withTeams;
//# sourceMappingURL=withTeams.jsx.map