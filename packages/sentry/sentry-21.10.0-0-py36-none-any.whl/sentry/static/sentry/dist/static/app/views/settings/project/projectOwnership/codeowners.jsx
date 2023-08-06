Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const rulesPanel_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectOwnership/rulesPanel"));
class CodeOwnersPanel extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleDelete = (codeowner) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, project, onDelete } = this.props;
            const endpoint = `/api/0/projects/${organization.slug}/${project.slug}/codeowners/${codeowner.id}/`;
            try {
                yield api.requestPromise(endpoint, {
                    method: 'DELETE',
                });
                onDelete(codeowner);
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Deletion successful'));
            }
            catch (_a) {
                // no 4xx errors should happen on delete
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred'));
            }
        });
        this.handleSync = (codeowner) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, project, onUpdate } = this.props;
            try {
                const codeownerFile = yield api.requestPromise(`/organizations/${organization.slug}/code-mappings/${codeowner.codeMappingId}/codeowners/`, {
                    method: 'GET',
                });
                const data = yield api.requestPromise(`/projects/${organization.slug}/${project.slug}/codeowners/${codeowner.id}/`, {
                    method: 'PUT',
                    data: { raw: codeownerFile.raw },
                });
                onUpdate(Object.assign(Object.assign({}, codeowner), data));
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('CODEOWNERS file sync successful.'));
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred trying to sync CODEOWNERS file.'));
            }
        });
    }
    render() {
        const { codeowners, disabled } = this.props;
        return codeowners.map(codeowner => {
            const { dateUpdated, provider, codeMapping, ownershipSyntax } = codeowner;
            return (<react_1.Fragment key={codeowner.id}>
          <rulesPanel_1.default data-test-id="codeowners-panel" type="codeowners" raw={ownershipSyntax || ''} dateUpdated={dateUpdated} provider={provider} repoName={codeMapping === null || codeMapping === void 0 ? void 0 : codeMapping.repoName} controls={[
                    <button_1.default key="sync" icon={<icons_1.IconSync size="xs"/>} size="xsmall" onClick={() => this.handleSync(codeowner)} disabled={disabled}/>,
                    <confirm_1.default onConfirm={() => this.handleDelete(codeowner)} message={(0, locale_1.t)('Are you sure you want to remove this CODEOWNERS file?')} key="confirm-delete" disabled={disabled}>
                <button_1.default key="delete" icon={<icons_1.IconDelete size="xs"/>} size="xsmall"/>
              </confirm_1.default>,
                ]}/>
        </react_1.Fragment>);
        });
    }
}
exports.default = (0, withApi_1.default)(CodeOwnersPanel);
//# sourceMappingURL=codeowners.jsx.map