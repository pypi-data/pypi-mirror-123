Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const intersection_1 = (0, tslib_1.__importDefault)(require("lodash/intersection"));
const indicator_1 = require("app/actionCreators/indicator");
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
/**
 * Given an array of scopes, return the choices the user has picked for each option
 * @param scopes {Array}
 */
const getPermissionSelectionsFromScopes = (scopes) => {
    const permissions = [];
    for (const permObj of constants_1.SENTRY_APP_PERMISSIONS) {
        let highestChoice;
        for (const perm in permObj.choices) {
            const choice = permObj.choices[perm];
            const scopesIntersection = (0, intersection_1.default)(choice.scopes, scopes);
            if (scopesIntersection.length > 0 &&
                scopesIntersection.length === choice.scopes.length) {
                if (!highestChoice || scopesIntersection.length > highestChoice.scopes.length) {
                    highestChoice = choice;
                }
            }
        }
        if (highestChoice) {
            // we can remove the read part of "Read & Write"
            const label = highestChoice.label.replace('Read & Write', 'Write');
            permissions.push(`${permObj.resource} ${label}`);
        }
    }
    return permissions;
};
class PublishRequestFormModel extends model_1.default {
    getTransformedData() {
        const data = this.getData();
        // map object to list of questions
        const questionnaire = Array.from(this.fieldDescriptor.values()).map(field => 
        // we read the meta for the question that has a react node for the label
        ({
            question: field.meta || field.label,
            answer: data[field.name],
        }));
        return { questionnaire };
    }
}
class SentryAppPublishRequestModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.form = new PublishRequestFormModel();
        this.handleSubmitSuccess = () => {
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Request to publish %s successful.', this.props.app.slug));
            this.props.closeModal();
        };
        this.handleSubmitError = err => {
            var _a;
            (0, indicator_1.addErrorMessage)((0, locale_1.tct)('Request to publish [app] fails. [detail]', {
                app: this.props.app.slug,
                detail: (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail,
            }));
        };
    }
    get formFields() {
        const { app } = this.props;
        const permissions = getPermissionSelectionsFromScopes(app.scopes);
        const permissionQuestionBaseText = 'Please justify why you are requesting each of the following permissions: ';
        const permissionQuestionPlainText = `${permissionQuestionBaseText}${permissions.join(', ')}.`;
        const permissionLabel = (<react_1.Fragment>
        <PermissionLabel>{permissionQuestionBaseText}</PermissionLabel>
        {permissions.map((permission, i) => (<react_1.Fragment key={permission}>
            {i > 0 && ', '} <Permission>{permission}</Permission>
          </react_1.Fragment>))}
        .
      </react_1.Fragment>);
        // No translations since we need to be able to read this email :)
        const baseFields = [
            {
                type: 'textarea',
                required: true,
                label: 'What does your integration do? Please be as detailed as possible.',
                autosize: true,
                rows: 1,
                inline: false,
                name: 'question0',
            },
            {
                type: 'textarea',
                required: true,
                label: 'What value does it offer customers?',
                autosize: true,
                rows: 1,
                inline: false,
                name: 'question1',
            },
            {
                type: 'textarea',
                required: true,
                label: 'Do you operate the web service your integration communicates with?',
                autosize: true,
                rows: 1,
                inline: false,
                name: 'question2',
            },
        ];
        // Only add the permissions question if there are perms to add
        if (permissions.length > 0) {
            baseFields.push({
                type: 'textarea',
                required: true,
                label: permissionLabel,
                autosize: true,
                rows: 1,
                inline: false,
                meta: permissionQuestionPlainText,
                name: 'question3',
            });
        }
        return baseFields;
    }
    render() {
        const { app, Header, Body } = this.props;
        const endpoint = `/sentry-apps/${app.slug}/publish-request/`;
        const forms = [
            {
                title: (0, locale_1.t)('Questions to answer'),
                fields: this.formFields,
            },
        ];
        return (<react_1.Fragment>
        <Header>{(0, locale_1.t)('Publish Request Questionnaire')}</Header>
        <Body>
          <Explanation>
            {(0, locale_1.t)(`Please fill out this questionnaire in order to get your integration evaluated for publication.
              Once your integration has been approved, users outside of your organization will be able to install it.`)}
          </Explanation>
          <form_1.default allowUndo apiMethod="POST" apiEndpoint={endpoint} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} model={this.form} submitLabel={(0, locale_1.t)('Request Publication')} onCancel={() => this.props.closeModal()}>
            <jsonForm_1.default forms={forms}/>
          </form_1.default>
        </Body>
      </react_1.Fragment>);
    }
}
exports.default = SentryAppPublishRequestModal;
const Explanation = (0, styled_1.default)('div') `
  margin: ${(0, space_1.default)(1.5)} 0px;
  font-size: 18px;
`;
const PermissionLabel = (0, styled_1.default)('span') `
  line-height: 24px;
`;
const Permission = (0, styled_1.default)('code') `
  line-height: 24px;
`;
//# sourceMappingURL=sentryAppPublishRequestModal.jsx.map