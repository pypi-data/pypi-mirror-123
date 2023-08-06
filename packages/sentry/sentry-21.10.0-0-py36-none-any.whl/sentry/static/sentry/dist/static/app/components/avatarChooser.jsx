Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar"));
const avatarCropper_1 = (0, tslib_1.__importDefault)(require("app/components/avatarCropper"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const well_1 = (0, tslib_1.__importDefault)(require("app/components/well"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const radioGroup_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/radioGroup"));
class AvatarChooser extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            model: this.props.model,
            savedDataUrl: null,
            dataUrl: null,
            hasError: false,
        };
        this.handleSaveSettings = (ev) => {
            const { endpoint, api } = this.props;
            const { model, dataUrl } = this.state;
            ev.preventDefault();
            let data = {};
            const avatarType = model && model.avatar ? model.avatar.avatarType : undefined;
            const avatarPhoto = dataUrl ? dataUrl.split(',')[1] : undefined;
            data = {
                avatar_photo: avatarPhoto,
                avatar_type: avatarType,
            };
            api.request(endpoint, {
                method: 'PUT',
                data,
                success: resp => {
                    this.setState({ savedDataUrl: this.state.dataUrl });
                    this.handleSuccess(resp);
                },
                error: this.handleError.bind(this, 'There was an error saving your preferences.'),
            });
        };
        this.handleChange = (id) => {
            var _a, _b;
            return this.updateState(Object.assign(Object.assign({}, this.state.model), { avatar: { avatarUuid: (_b = (_a = this.state.model.avatar) === null || _a === void 0 ? void 0 : _a.avatarUuid) !== null && _b !== void 0 ? _b : '', avatarType: id } }));
        };
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        // Update local state if defined in props
        if (typeof nextProps.model !== 'undefined') {
            this.setState({ model: nextProps.model });
        }
    }
    updateState(model) {
        this.setState({ model });
    }
    handleError(msg) {
        (0, indicator_1.addErrorMessage)(msg);
    }
    handleSuccess(model) {
        const { onSave } = this.props;
        this.setState({ model });
        onSave(model);
        (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Successfully saved avatar preferences'));
    }
    render() {
        var _a, _b;
        const { allowGravatar, allowUpload, allowLetter, savedDataUrl, type, isUser, disabled, } = this.props;
        const { hasError, model } = this.state;
        if (hasError) {
            return <loadingError_1.default />;
        }
        if (!model) {
            return <loadingIndicator_1.default />;
        }
        const avatarType = (_b = (_a = model.avatar) === null || _a === void 0 ? void 0 : _a.avatarType) !== null && _b !== void 0 ? _b : 'letter_avatar';
        const isLetter = avatarType === 'letter_avatar';
        const isTeam = type === 'team';
        const isOrganization = type === 'organization';
        const choices = [];
        if (allowLetter) {
            choices.push(['letter_avatar', (0, locale_1.t)('Use initials')]);
        }
        if (allowUpload) {
            choices.push(['upload', (0, locale_1.t)('Upload an image')]);
        }
        if (allowGravatar) {
            choices.push(['gravatar', (0, locale_1.t)('Use Gravatar')]);
        }
        return (<panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Avatar')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <AvatarForm>
            <AvatarGroup inline={isLetter}>
              <radioGroup_1.default style={{ flex: 1 }} choices={choices} value={avatarType} label={(0, locale_1.t)('Avatar Type')} onChange={this.handleChange} disabled={disabled}/>
              {isLetter && (<avatar_1.default gravatar={false} style={{ width: 90, height: 90 }} user={isUser ? model : undefined} organization={isOrganization ? model : undefined} team={isTeam ? model : undefined}/>)}
            </AvatarGroup>

            <AvatarUploadSection>
              {allowGravatar && avatarType === 'gravatar' && (<well_1.default>
                  {(0, locale_1.t)('Gravatars are managed through ')}
                  <externalLink_1.default href="http://gravatar.com">Gravatar.com</externalLink_1.default>
                </well_1.default>)}

              {model.avatar && avatarType === 'upload' && (<avatarCropper_1.default {...this.props} type={type} model={model} savedDataUrl={savedDataUrl} updateDataUrlState={dataState => this.setState(dataState)}/>)}
              <AvatarSubmit className="form-actions">
                <button_1.default type="button" priority="primary" onClick={this.handleSaveSettings} disabled={disabled}>
                  {(0, locale_1.t)('Save Avatar')}
                </button_1.default>
              </AvatarSubmit>
            </AvatarUploadSection>
          </AvatarForm>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
AvatarChooser.defaultProps = {
    allowGravatar: true,
    allowLetter: true,
    allowUpload: true,
    type: 'user',
    onSave: () => { },
};
const AvatarGroup = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: ${p => (p.inline ? 'row' : 'column')};
`;
const AvatarForm = (0, styled_1.default)('div') `
  line-height: 1.5em;
  padding: 1em 1.25em;
`;
const AvatarSubmit = (0, styled_1.default)('fieldset') `
  display: flex;
  justify-content: flex-end;
  margin-top: 1em;
`;
const AvatarUploadSection = (0, styled_1.default)('div') `
  margin-top: 1em;
`;
exports.default = (0, withApi_1.default)(AvatarChooser);
//# sourceMappingURL=avatarChooser.jsx.map