Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const locale_1 = require("app/locale");
const callIfFunction_1 = require("app/utils/callIfFunction");
const slugify_1 = (0, tslib_1.__importDefault)(require("app/utils/slugify"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textField"));
class CreateTeamForm extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleSubmit = (data, onSuccess, onError) => {
            (0, callIfFunction_1.callIfFunction)(this.props.onSubmit, data, onSuccess, onError);
        };
        this.handleCreateTeamSuccess = (data) => {
            (0, callIfFunction_1.callIfFunction)(this.props.onSuccess, data);
        };
    }
    render() {
        const { organization } = this.props;
        return (<react_1.Fragment>
        <p>
          {(0, locale_1.t)('Members of a team have access to specific areas, such as a new release or a new application feature.')}
        </p>

        <form_1.default submitLabel={(0, locale_1.t)('Create Team')} apiEndpoint={`/organizations/${organization.slug}/teams/`} apiMethod="POST" onSubmit={this.handleSubmit} onSubmitSuccess={this.handleCreateTeamSuccess} requireChanges data-test-id="create-team-form" {...this.props.formProps}>
          <textField_1.default name="slug" label={(0, locale_1.t)('Team Name')} placeholder={(0, locale_1.t)('e.g. operations, web-frontend, desktop')} help={(0, locale_1.t)('May contain lowercase letters, numbers, dashes and underscores.')} required stacked flexibleControlStateSize inline={false} transformInput={slugify_1.default}/>
        </form_1.default>
      </react_1.Fragment>);
    }
}
exports.default = CreateTeamForm;
//# sourceMappingURL=createTeamForm.jsx.map