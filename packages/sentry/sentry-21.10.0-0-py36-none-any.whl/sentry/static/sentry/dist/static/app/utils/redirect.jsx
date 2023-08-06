Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
// This is react-router v4 <Redirect to="path/" /> component to allow things
// to be declarative.
function Redirect({ to, router }) {
    // Redirect on mount.
    (0, react_1.useEffect)(() => router.replace(to), []);
    return null;
}
exports.default = Redirect;
//# sourceMappingURL=redirect.jsx.map