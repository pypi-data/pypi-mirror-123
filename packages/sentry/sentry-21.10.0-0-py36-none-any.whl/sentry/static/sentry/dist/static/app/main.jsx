Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const demoHeader_1 = (0, tslib_1.__importDefault)(require("app/components/demo/demoHeader"));
const themeAndStyleProvider_1 = (0, tslib_1.__importDefault)(require("app/components/themeAndStyleProvider"));
const routes_1 = (0, tslib_1.__importDefault)(require("app/routes"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
function Main() {
    return (<themeAndStyleProvider_1.default>
      {configStore_1.default.get('demoMode') && <demoHeader_1.default />}
      <react_router_1.Router history={react_router_1.browserHistory}>{(0, routes_1.default)()}</react_router_1.Router>
    </themeAndStyleProvider_1.default>);
}
exports.default = Main;
//# sourceMappingURL=main.jsx.map