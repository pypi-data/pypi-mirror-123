Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const builtInRepositories_1 = (0, tslib_1.__importDefault)(require("./builtInRepositories"));
const customRepositories_1 = (0, tslib_1.__importDefault)(require("./customRepositories"));
function ExternalSources({ api, organization, customRepositories, builtinSymbolSources, builtinSymbolSourceOptions, projSlug, location, router, }) {
    return (<react_1.Fragment>
      <builtInRepositories_1.default api={api} organization={organization} builtinSymbolSources={builtinSymbolSources} builtinSymbolSourceOptions={builtinSymbolSourceOptions} projSlug={projSlug}/>
      <customRepositories_1.default api={api} location={location} router={router} organization={organization} customRepositories={customRepositories} projSlug={projSlug}/>
    </react_1.Fragment>);
}
exports.default = ExternalSources;
//# sourceMappingURL=index.jsx.map