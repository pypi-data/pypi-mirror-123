Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const react_2 = require("@emotion/react");
const debugFileSources_1 = require("app/data/debugFileSources");
const locale_1 = require("app/locale");
const debugFiles_1 = require("app/types/debugFiles");
const fieldFromConfig_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/fieldFromConfig"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const appStoreConnect_1 = (0, tslib_1.__importDefault)(require("./appStoreConnect"));
const http_1 = (0, tslib_1.__importDefault)(require("./http"));
const utils_1 = require("./utils");
function DebugFileCustomRepository({ Header, Body, Footer, onSave, sourceConfig, sourceType, params: { orgId, projectId: projectSlug }, location, appStoreConnectContext, closeModal, }) {
    function handleSave(data) {
        if (!data) {
            closeModal();
            window.location.reload();
            return;
        }
        onSave(Object.assign(Object.assign({}, (0, utils_1.getFinalData)(sourceType, data)), { type: sourceType })).then(() => {
            closeModal();
        });
    }
    if (sourceType === debugFiles_1.CustomRepoType.APP_STORE_CONNECT) {
        return (<appStoreConnect_1.default Header={Header} Body={Body} Footer={Footer} orgSlug={orgId} projectSlug={projectSlug} onSubmit={handleSave} initialData={sourceConfig} location={location} appStoreConnectContext={appStoreConnectContext}/>);
    }
    if (sourceType === debugFiles_1.CustomRepoType.HTTP) {
        return (<http_1.default Header={Header} Body={Body} Footer={Footer} onSubmit={handleSave} initialData={sourceConfig}/>);
    }
    const { initialData, fields } = (0, utils_1.getFormFieldsAndInitialData)(sourceType, sourceConfig);
    return (<react_1.Fragment>
      <Header closeButton>
        {sourceConfig
            ? (0, locale_1.tct)('Update [name] Repository', { name: (0, debugFileSources_1.getDebugSourceName)(sourceType) })
            : (0, locale_1.tct)('Add [name] Repository', { name: (0, debugFileSources_1.getDebugSourceName)(sourceType) })}
      </Header>
      {fields && (<form_1.default allowUndo requireChanges initialData={initialData} onSubmit={handleSave} footerClass="modal-footer">
          {fields.map((field, i) => (<fieldFromConfig_1.default key={field.name || i} field={field} inline={false} stacked/>))}
        </form_1.default>)}
    </react_1.Fragment>);
}
exports.default = (0, react_router_1.withRouter)(DebugFileCustomRepository);
exports.modalCss = (0, react_2.css) `
  width: 100%;
  max-width: 680px;
`;
//# sourceMappingURL=index.jsx.map