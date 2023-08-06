Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const userFeedback_1 = (0, tslib_1.__importDefault)(require("app/data/forms/userFeedback"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
class ProjectUserFeedbackSettings extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleClick = () => {
            Sentry.showReportDialog({
                // should never make it to the Sentry API, but just in case, use throwaway id
                eventId: '00000000000000000000000000000000',
            });
        };
    }
    componentDidMount() {
        window.sentryEmbedCallback = function (embed) {
            // Mock the embed's submit xhr to always be successful
            // NOTE: this will not have errors if the form is empty
            embed.submit = function (_body) {
                this._submitInProgress = true;
                setTimeout(() => {
                    this._submitInProgress = false;
                    this.onSuccess();
                }, 500);
            };
        };
    }
    componentWillUnmount() {
        window.sentryEmbedCallback = null;
    }
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [
            ['keyList', `/projects/${orgId}/${projectId}/keys/`],
            ['project', `/projects/${orgId}/${projectId}/`],
        ];
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('User Feedback'), projectId, false);
    }
    renderBody() {
        const { orgId, projectId } = this.props.params;
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('User Feedback')}/>
        <textBlock_1.default>
          {(0, locale_1.t)(`Don't rely on stack traces and graphs alone to understand
            the cause and impact of errors. Enable User Feedback to collect
            your users' comments when they encounter a crash or bug.`)}
        </textBlock_1.default>
        <textBlock_1.default>
          {(0, locale_1.t)(`When configured, your users will be presented with a dialog prompting
            them for additional information. That information will get attached to
            the issue in Sentry.`)}
        </textBlock_1.default>
        <ButtonList>
          <button_1.default external href="https://docs.sentry.io/product/user-feedback/">
            {(0, locale_1.t)('Read the docs')}
          </button_1.default>
          <button_1.default priority="primary" onClick={this.handleClick}>
            {(0, locale_1.t)('Open the report dialog')}
          </button_1.default>
        </ButtonList>

        <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint={`/projects/${orgId}/${projectId}/`} initialData={this.state.project.options}>
          <access_1.default access={['project:write']}>
            {({ hasAccess }) => <jsonForm_1.default disabled={!hasAccess} forms={userFeedback_1.default}/>}
          </access_1.default>
        </form_1.default>
      </div>);
    }
}
const ButtonList = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
  margin-bottom: ${(0, space_1.default)(2)};
`;
exports.default = ProjectUserFeedbackSettings;
//# sourceMappingURL=projectUserFeedback.jsx.map