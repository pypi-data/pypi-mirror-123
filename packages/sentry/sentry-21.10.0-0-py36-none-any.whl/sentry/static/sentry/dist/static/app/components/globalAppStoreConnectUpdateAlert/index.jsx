Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const AppStoreConnectContext = (0, tslib_1.__importStar)(require("app/components/projects/appStoreConnectContext"));
const updateAlert_1 = (0, tslib_1.__importDefault)(require("./updateAlert"));
function GlobalAppStoreConnectUpdateAlert(_a) {
    var { project, organization } = _a, rest = (0, tslib_1.__rest)(_a, ["project", "organization"]);
    return (<AppStoreConnectContext.Provider project={project} organization={organization}>
      <updateAlert_1.default project={project} organization={organization} {...rest}/>
    </AppStoreConnectContext.Provider>);
}
exports.default = GlobalAppStoreConnectUpdateAlert;
//# sourceMappingURL=index.jsx.map