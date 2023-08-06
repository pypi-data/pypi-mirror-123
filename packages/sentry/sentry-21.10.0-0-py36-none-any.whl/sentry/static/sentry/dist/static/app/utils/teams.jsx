Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const useTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/useTeams"));
/**
 * This is a utility component to leverage the useTeams hook to provide
 * a render props component which returns teams through a variety of inputs
 * such as a list of slugs or user teams.
 */
function Teams(_a) {
    var { children } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
    const renderProps = (0, useTeams_1.default)(props);
    return <react_1.Fragment>{children(renderProps)}</react_1.Fragment>;
}
exports.default = Teams;
//# sourceMappingURL=teams.jsx.map