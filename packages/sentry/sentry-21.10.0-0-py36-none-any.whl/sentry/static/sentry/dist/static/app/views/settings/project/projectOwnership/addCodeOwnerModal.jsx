Object.defineProperty(exports, "__esModule", { value: true });
exports.AddCodeOwnerModal = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
class AddCodeOwnerModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            codeownersFile: null,
            codeMappingId: null,
            isLoading: false,
            error: false,
            errorJSON: null,
        };
        this.fetchFile = (codeMappingId) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization } = this.props;
            this.setState({
                codeMappingId,
                codeownersFile: null,
                error: false,
                errorJSON: null,
                isLoading: true,
            });
            try {
                const data = yield this.props.api.requestPromise(`/organizations/${organization.slug}/code-mappings/${codeMappingId}/codeowners/`, {
                    method: 'GET',
                });
                this.setState({ codeownersFile: data, isLoading: false });
            }
            catch (_err) {
                this.setState({ isLoading: false });
            }
        });
        this.addFile = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, project, codeMappings } = this.props;
            const { codeownersFile, codeMappingId } = this.state;
            if (codeownersFile) {
                const postData = {
                    codeMappingId,
                    raw: codeownersFile.raw,
                };
                try {
                    const data = yield this.props.api.requestPromise(`/projects/${organization.slug}/${project.slug}/codeowners/`, {
                        method: 'POST',
                        data: postData,
                    });
                    const codeMapping = codeMappings.find(mapping => mapping.id === (codeMappingId === null || codeMappingId === void 0 ? void 0 : codeMappingId.toString()));
                    this.handleAddedFile(Object.assign(Object.assign({}, data), { codeMapping }));
                }
                catch (err) {
                    if (err.responseJSON.raw) {
                        this.setState({ error: true, errorJSON: err.responseJSON, isLoading: false });
                    }
                    else {
                        (0, indicator_1.addErrorMessage)((0, locale_1.t)(Object.values(err.responseJSON).flat().join(' ')));
                    }
                }
            }
        });
    }
    handleAddedFile(data) {
        this.props.onSave(data);
        this.props.closeModal();
    }
    sourceFile(codeownersFile) {
        return (<panels_1.Panel>
        <SourceFileBody>
          <icons_1.IconCheckmark size="md" isCircled color="green200"/>
          {codeownersFile.filepath}
          <button_1.default size="small" href={codeownersFile.html_url} target="_blank">
            {(0, locale_1.t)('Preview File')}
          </button_1.default>
        </SourceFileBody>
      </panels_1.Panel>);
    }
    errorMessage(baseUrl) {
        var _a;
        const { errorJSON, codeMappingId } = this.state;
        const { codeMappings } = this.props;
        const codeMapping = codeMappings.find(mapping => mapping.id === codeMappingId);
        const { integrationId, provider } = codeMapping;
        const errActors = (_a = errorJSON === null || errorJSON === void 0 ? void 0 : errorJSON.raw) === null || _a === void 0 ? void 0 : _a[0].split('\n').map((el, i) => <p key={i}>{el}</p>);
        return (<alert_1.default type="error" icon={<icons_1.IconNot size="md"/>}>
        {errActors}
        {codeMapping && (<p>
            {(0, locale_1.tct)('Configure [userMappingsLink:User Mappings] or [teamMappingsLink:Team Mappings] for any missing associations.', {
                    userMappingsLink: (<link_1.default to={`${baseUrl}/${provider === null || provider === void 0 ? void 0 : provider.key}/${integrationId}/?tab=userMappings&referrer=add-codeowners`}/>),
                    teamMappingsLink: (<link_1.default to={`${baseUrl}/${provider === null || provider === void 0 ? void 0 : provider.key}/${integrationId}/?tab=teamMappings&referrer=add-codeowners`}/>),
                })}
          </p>)}
        {(0, locale_1.tct)('[addAndSkip:Add and Skip Missing Associations] will add your codeowner file and skip any rules that having missing associations. You can add associations later for any skipped rules.', { addAndSkip: <strong>Add and Skip Missing Associations</strong> })}
      </alert_1.default>);
    }
    noSourceFile() {
        const { codeMappingId, isLoading } = this.state;
        if (isLoading) {
            return (<Container>
          <loadingIndicator_1.default mini/>
        </Container>);
        }
        if (!codeMappingId) {
            return null;
        }
        return (<panels_1.Panel>
        <NoSourceFileBody>
          {codeMappingId ? (<react_1.Fragment>
              <icons_1.IconNot size="md" color="red200"/>
              {(0, locale_1.t)('No codeowner file found.')}
            </react_1.Fragment>) : null}
        </NoSourceFileBody>
      </panels_1.Panel>);
    }
    render() {
        const { Header, Body, Footer } = this.props;
        const { codeownersFile, error, errorJSON } = this.state;
        const { codeMappings, integrations, organization } = this.props;
        const baseUrl = `/settings/${organization.slug}/integrations`;
        return (<react_1.Fragment>
        <Header closeButton>{(0, locale_1.t)('Add Code Owner File')}</Header>
        <Body>
          {!codeMappings.length && (<react_1.Fragment>
              <div>
                {(0, locale_1.t)("Configure code mapping to add your CODEOWNERS file. Select the integration you'd like to use for mapping:")}
              </div>
              <IntegrationsList>
                {integrations.map(integration => (<button_1.default key={integration.id} type="button" to={`${baseUrl}/${integration.provider.key}/${integration.id}/?tab=codeMappings&referrer=add-codeowners`}>
                    {(0, integrationUtil_1.getIntegrationIcon)(integration.provider.key)}
                    <IntegrationName>{integration.name}</IntegrationName>
                  </button_1.default>))}
              </IntegrationsList>
            </react_1.Fragment>)}
          {codeMappings.length > 0 && (<form_1.default apiMethod="POST" apiEndpoint="/code-mappings/" hideFooter initialData={{}}>
              <StyledSelectField name="codeMappingId" label={(0, locale_1.t)('Apply an existing code mapping')} choices={codeMappings.map((cm) => [
                    cm.id,
                    cm.repoName,
                ])} onChange={this.fetchFile} required inline={false} flexibleControlStateSize stacked/>

              <FileResult>
                {codeownersFile ? this.sourceFile(codeownersFile) : this.noSourceFile()}
                {error && errorJSON && this.errorMessage(baseUrl)}
              </FileResult>
            </form_1.default>)}
        </Body>
        <Footer>
          <button_1.default disabled={codeownersFile ? false : true} label={(0, locale_1.t)('Add File')} priority="primary" onClick={this.addFile}>
            {(0, locale_1.t)('Add File')}
          </button_1.default>
        </Footer>
      </react_1.Fragment>);
    }
}
exports.AddCodeOwnerModal = AddCodeOwnerModal;
exports.default = (0, withApi_1.default)(AddCodeOwnerModal);
const StyledSelectField = (0, styled_1.default)(selectField_1.default) `
  border-bottom: None;
  padding-right: 16px;
`;
const FileResult = (0, styled_1.default)('div') `
  width: inherit;
`;
const NoSourceFileBody = (0, styled_1.default)(panels_1.PanelBody) `
  display: grid;
  padding: 12px;
  grid-template-columns: 30px 1fr;
  align-items: center;
`;
const SourceFileBody = (0, styled_1.default)(panels_1.PanelBody) `
  display: grid;
  padding: 12px;
  grid-template-columns: 30px 1fr 100px;
  align-items: center;
`;
const IntegrationsList = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  justify-items: center;
  margin-top: ${(0, space_1.default)(2)};
`;
const IntegrationName = (0, styled_1.default)('p') `
  padding-left: 10px;
`;
const Container = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
`;
//# sourceMappingURL=addCodeOwnerModal.jsx.map