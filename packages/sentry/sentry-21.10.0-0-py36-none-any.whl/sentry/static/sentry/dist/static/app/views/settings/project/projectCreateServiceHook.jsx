Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const locale_1 = require("app/locale");
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const serviceHookSettingsForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/serviceHookSettingsForm"));
function ProjectCreateServiceHook({ params }) {
    const { orgId, projectId } = params;
    const title = (0, locale_1.t)('Create Service Hook');
    return (<react_document_title_1.default title={`${title} - Sentry`}>
      <react_1.Fragment>
        <settingsPageHeader_1.default title={title}/>
        <serviceHookSettingsForm_1.default orgId={orgId} projectId={projectId} initialData={{ events: [], isActive: true }}/>
      </react_1.Fragment>
    </react_document_title_1.default>);
}
exports.default = ProjectCreateServiceHook;
//# sourceMappingURL=projectCreateServiceHook.jsx.map