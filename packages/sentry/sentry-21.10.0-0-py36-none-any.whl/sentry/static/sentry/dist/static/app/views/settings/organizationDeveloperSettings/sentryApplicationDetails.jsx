Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const mobx_react_1 = require("mobx-react");
const scroll_to_element_1 = (0, tslib_1.__importDefault)(require("scroll-to-element"));
const indicator_1 = require("app/actionCreators/indicator");
const sentryAppTokens_1 = require("app/actionCreators/sentryAppTokens");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const constants_1 = require("app/constants");
const sentryApplication_1 = require("app/data/forms/sentryApplication");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const permissionsObserver_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organizationDeveloperSettings/permissionsObserver"));
/**
 * Finds the resource in SENTRY_APP_PERMISSIONS that contains a given scope
 * We should always find a match unless there is a bug
 * @param {Scope} scope
 * @return {Resource | undefined}
 */
const getResourceFromScope = (scope) => {
    for (const permObj of constants_1.SENTRY_APP_PERMISSIONS) {
        const allChoices = Object.values(permObj.choices);
        const allScopes = allChoices.reduce((_allScopes, choice) => { var _a; return _allScopes.concat((_a = choice === null || choice === void 0 ? void 0 : choice.scopes) !== null && _a !== void 0 ? _a : []); }, []);
        if (allScopes.includes(scope)) {
            return permObj.resource;
        }
    }
    return undefined;
};
class SentryAppFormModel extends model_1.default {
    /**
     * Filter out Permission input field values.
     *
     * Permissions (API Scopes) are presented as a list of SelectFields.
     * Instead of them being submitted individually, we want them rolled
     * up into a single list of scopes (this is done in `PermissionSelection`).
     *
     * Because they are all individual inputs, we end up with attributes
     * in the JSON we send to the API that we don't want.
     *
     * This function filters those attributes out of the data that is
     * ultimately sent to the API.
     */
    getData() {
        return this.fields.toJSON().reduce((data, [k, v]) => {
            if (!k.endsWith('--permission')) {
                data[k] = v;
            }
            return data;
        }, {});
    }
    /**
     * We need to map the API response errors to the actual form fields.
     * We do this by pulling out scopes and mapping each scope error to the correct input.
     * @param {Object} responseJSON
     */
    mapFormErrors(responseJSON) {
        if (!responseJSON) {
            return responseJSON;
        }
        const formErrors = (0, omit_1.default)(responseJSON, ['scopes']);
        if (responseJSON.scopes) {
            responseJSON.scopes.forEach((message) => {
                // find the scope from the error message of a specific format
                const matches = message.match(/Requested permission of (\w+:\w+)/);
                if (matches) {
                    const scope = matches[1];
                    const resource = getResourceFromScope(scope);
                    // should always match but technically resource can be undefined
                    if (resource) {
                        formErrors[`${resource}--permission`] = [message];
                    }
                }
            });
        }
        return formErrors;
    }
}
class SentryApplicationDetails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.form = new SentryAppFormModel();
        this.handleSubmitSuccess = (data) => {
            const { app } = this.state;
            const { orgId } = this.props.params;
            const baseUrl = `/settings/${orgId}/developer-settings/`;
            const url = app ? baseUrl : `${baseUrl}${data.slug}/`;
            if (app) {
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('%s successfully saved.', data.name));
            }
            else {
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('%s successfully created.', data.name));
            }
            react_router_1.browserHistory.push(url);
        };
        this.handleSubmitError = err => {
            var _a;
            let errorMessage = (0, locale_1.t)('Unknown Error');
            if (err.status >= 400 && err.status < 500) {
                errorMessage = (_a = err === null || err === void 0 ? void 0 : err.responseJSON.detail) !== null && _a !== void 0 ? _a : errorMessage;
            }
            (0, indicator_1.addErrorMessage)(errorMessage);
            if (this.form.formErrors) {
                const firstErrorFieldId = Object.keys(this.form.formErrors)[0];
                if (firstErrorFieldId) {
                    (0, scroll_to_element_1.default)(`#${firstErrorFieldId}`, {
                        align: 'middle',
                        offset: 0,
                    });
                }
            }
        };
        this.onAddToken = (evt) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            evt.preventDefault();
            const { app, tokens } = this.state;
            if (!app) {
                return;
            }
            const api = this.api;
            const token = yield (0, sentryAppTokens_1.addSentryAppToken)(api, app);
            const newTokens = tokens.concat(token);
            this.setState({ tokens: newTokens });
        });
        this.onRemoveToken = (token, evt) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            evt.preventDefault();
            const { app, tokens } = this.state;
            if (!app) {
                return;
            }
            const api = this.api;
            const newTokens = tokens.filter(tok => tok.token !== token.token);
            yield (0, sentryAppTokens_1.removeSentryAppToken)(api, app, token.token);
            this.setState({ tokens: newTokens });
        });
        this.renderTokens = () => {
            const { tokens } = this.state;
            if (tokens.length > 0) {
                return tokens.map(token => (<StyledPanelItem key={token.token}>
          <TokenItem>
            <tooltip_1.default disabled={this.showAuthInfo} position="right" containerDisplayMode="inline" title={(0, locale_1.t)('You do not have access to view these credentials because the permissions for this integration exceed those of your role.')}>
              <textCopyInput_1.default>
                {(0, getDynamicText_1.default)({ value: token.token, fixed: 'xxxxxx' })}
              </textCopyInput_1.default>
            </tooltip_1.default>
          </TokenItem>
          <CreatedDate>
            <CreatedTitle>Created:</CreatedTitle>
            <dateTime_1.default date={(0, getDynamicText_1.default)({
                        value: token.dateCreated,
                        fixed: new Date(1508208080000),
                    })}/>
          </CreatedDate>
          <button_1.default onClick={this.onRemoveToken.bind(this, token)} size="small" icon={<icons_1.IconDelete />} data-test-id="token-delete" type="button">
            {(0, locale_1.t)('Revoke')}
          </button_1.default>
        </StyledPanelItem>));
            }
            else {
                return <emptyMessage_1.default description={(0, locale_1.t)('No tokens created yet.')}/>;
            }
        };
        this.onFieldChange = (name, value) => {
            if (name === 'webhookUrl' && !value && this.isInternal) {
                // if no webhook, then set isAlertable to false
                this.form.setValue('isAlertable', false);
            }
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { app: null, tokens: [] });
    }
    getEndpoints() {
        const { appSlug } = this.props.params;
        if (appSlug) {
            return [
                ['app', `/sentry-apps/${appSlug}/`],
                ['tokens', `/sentry-apps/${appSlug}/api-tokens/`],
            ];
        }
        return [];
    }
    getTitle() {
        const { orgId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Sentry Integration Details'), orgId, false);
    }
    // Events may come from the API as "issue.created" when we just want "issue" here.
    normalize(events) {
        if (events.length === 0) {
            return events;
        }
        return events.map(e => e.split('.').shift());
    }
    get isInternal() {
        const { app } = this.state;
        if (app) {
            // if we are editing an existing app, check the status of the app
            return app.status === 'internal';
        }
        return this.props.route.path === 'new-internal/';
    }
    get showAuthInfo() {
        const { app } = this.state;
        return !(app && app.clientSecret && app.clientSecret[0] === '*');
    }
    renderBody() {
        const { orgId } = this.props.params;
        const { app } = this.state;
        const scopes = (app && [...app.scopes]) || [];
        const events = (app && this.normalize(app.events)) || [];
        const method = app ? 'PUT' : 'POST';
        const endpoint = app ? `/sentry-apps/${app.slug}/` : '/sentry-apps/';
        const forms = this.isInternal ? sentryApplication_1.internalIntegrationForms : sentryApplication_1.publicIntegrationForms;
        let verifyInstall;
        if (this.isInternal) {
            // force verifyInstall to false for all internal apps
            verifyInstall = false;
        }
        else {
            // use the existing value for verifyInstall if the app exists, otherwise default to true
            verifyInstall = app ? app.verifyInstall : true;
        }
        return (<div>
        <settingsPageHeader_1.default title={this.getTitle()}/>
        <form_1.default apiMethod={method} apiEndpoint={endpoint} allowUndo initialData={Object.assign(Object.assign({ organization: orgId, isAlertable: false, isInternal: this.isInternal, schema: {}, scopes: [] }, app), { verifyInstall })} model={this.form} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onFieldChange={this.onFieldChange}>
          <mobx_react_1.Observer>
            {() => {
                const webhookDisabled = this.isInternal && !this.form.getValue('webhookUrl');
                return (<React.Fragment>
                  <jsonForm_1.default additionalFieldProps={{ webhookDisabled }} forms={forms}/>

                  <permissionsObserver_1.default webhookDisabled={webhookDisabled} appPublished={app ? app.status === 'published' : false} scopes={scopes} events={events}/>
                </React.Fragment>);
            }}
          </mobx_react_1.Observer>

          {app && app.status === 'internal' && (<panels_1.Panel>
              <panels_1.PanelHeader hasButtons>
                {(0, locale_1.t)('Tokens')}
                <button_1.default size="xsmall" icon={<icons_1.IconAdd size="xs" isCircled/>} onClick={evt => this.onAddToken(evt)} data-test-id="token-add" type="button">
                  {(0, locale_1.t)('New Token')}
                </button_1.default>
              </panels_1.PanelHeader>
              <panels_1.PanelBody>{this.renderTokens()}</panels_1.PanelBody>
            </panels_1.Panel>)}

          {app && (<panels_1.Panel>
              <panels_1.PanelHeader>{(0, locale_1.t)('Credentials')}</panels_1.PanelHeader>
              <panels_1.PanelBody>
                {app.status !== 'internal' && (<formField_1.default name="clientId" label="Client ID">
                    {({ value }) => (<textCopyInput_1.default>
                        {(0, getDynamicText_1.default)({ value, fixed: 'CI_CLIENT_ID' })}
                      </textCopyInput_1.default>)}
                  </formField_1.default>)}
                <formField_1.default name="clientSecret" label="Client Secret">
                  {({ value }) => value ? (<tooltip_1.default disabled={this.showAuthInfo} position="right" containerDisplayMode="inline" title={(0, locale_1.t)('You do not have access to view these credentials because the permissions for this integration exceed those of your role.')}>
                        <textCopyInput_1.default>
                          {(0, getDynamicText_1.default)({ value, fixed: 'CI_CLIENT_SECRET' })}
                        </textCopyInput_1.default>
                      </tooltip_1.default>) : (<em>hidden</em>)}
                </formField_1.default>
              </panels_1.PanelBody>
            </panels_1.Panel>)}
        </form_1.default>
      </div>);
    }
}
exports.default = SentryApplicationDetails;
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  display: flex;
  justify-content: space-between;
`;
const TokenItem = (0, styled_1.default)('div') `
  width: 70%;
`;
const CreatedTitle = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray300};
  margin-bottom: 2px;
`;
const CreatedDate = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  font-size: 14px;
  margin: 0 10px;
`;
//# sourceMappingURL=sentryApplicationDetails.jsx.map