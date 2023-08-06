Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_autosize_textarea_1 = (0, tslib_1.__importDefault)(require("react-autosize-textarea"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const api_1 = require("app/api");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const input_1 = require("app/styles/input");
const utils_1 = require("app/utils");
const ruleBuilder_1 = (0, tslib_1.__importDefault)(require("./ruleBuilder"));
const defaultProps = {
    urls: [],
    paths: [],
    disabled: false,
};
class OwnerInput extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            hasChanges: false,
            text: null,
            error: null,
        };
        this.handleUpdateOwnership = () => {
            const { organization, project, onSave } = this.props;
            const { text } = this.state;
            this.setState({ error: null });
            const api = new api_1.Client();
            const request = api.requestPromise(`/projects/${organization.slug}/${project.slug}/ownership/`, {
                method: 'PUT',
                data: { raw: text || '' },
            });
            request
                .then(() => {
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Updated issue ownership rules'));
                this.setState({
                    hasChanges: false,
                    text,
                }, () => onSave && onSave(text));
            })
                .catch(error => {
                this.setState({ error: error.responseJSON });
                if (error.status === 403) {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)("You don't have permission to modify issue ownership rules for this project"));
                }
                else if (error.status === 400 &&
                    error.responseJSON.raw &&
                    error.responseJSON.raw[0].startsWith('Invalid rule owners:')) {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to save issue ownership rule changes: ' + error.responseJSON.raw[0]));
                }
                else {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to save issue ownership rule changes'));
                }
            });
            return request;
        };
        this.handleChange = (e) => {
            this.setState({
                hasChanges: true,
                text: e.target.value,
            });
        };
        this.handleAddRule = (rule) => {
            const { initialText } = this.props;
            this.setState(({ text }) => ({
                text: (text || initialText) + '\n' + rule,
            }), this.handleUpdateOwnership);
        };
    }
    parseError(error) {
        var _a, _b, _c;
        const text = (_a = error === null || error === void 0 ? void 0 : error.raw) === null || _a === void 0 ? void 0 : _a[0];
        if (!text) {
            return null;
        }
        if (text.startsWith('Invalid rule owners:')) {
            return <InvalidOwners>{text}</InvalidOwners>;
        }
        else {
            return (<SyntaxOverlay line={parseInt((_c = (_b = text.match(/line (\d*),/)) === null || _b === void 0 ? void 0 : _b[1]) !== null && _c !== void 0 ? _c : '', 10) - 1}/>);
        }
    }
    mentionableUsers() {
        return memberListStore_1.default.getAll().map(member => ({
            id: member.id,
            display: member.email,
            email: member.email,
        }));
    }
    mentionableTeams() {
        const { project } = this.props;
        const projectWithTeams = projectsStore_1.default.getBySlug(project.slug);
        if (!projectWithTeams) {
            return [];
        }
        return projectWithTeams.teams.map((team) => ({
            id: team.id,
            display: `#${team.slug}`,
            email: team.id,
        }));
    }
    render() {
        const { project, organization, disabled, urls, paths, initialText } = this.props;
        const { hasChanges, text, error } = this.state;
        return (<React.Fragment>
        <ruleBuilder_1.default urls={urls} paths={paths} organization={organization} project={project} onAddRule={this.handleAddRule.bind(this)} disabled={disabled}/>
        <div style={{ position: 'relative' }} onKeyDown={e => {
                if (e.metaKey && e.key === 'Enter') {
                    this.handleUpdateOwnership();
                }
            }}>
          <StyledTextArea placeholder={'#example usage\n' +
                'path:src/example/pipeline/* person@sentry.io #infra\n' +
                'url:http://example.com/settings/* #product\n' +
                'tags.sku_class:enterprise #enterprise'} onChange={this.handleChange} disabled={disabled} value={(0, utils_1.defined)(text) ? text : initialText} spellCheck="false" autoComplete="off" autoCorrect="off" autoCapitalize="off"/>
          <ActionBar>
            <div>{this.parseError(error)}</div>
            <SaveButton>
              <button_1.default size="small" priority="primary" onClick={this.handleUpdateOwnership} disabled={disabled || !hasChanges}>
                {(0, locale_1.t)('Save Changes')}
              </button_1.default>
            </SaveButton>
          </ActionBar>
        </div>
      </React.Fragment>);
    }
}
OwnerInput.defaultProps = defaultProps;
const TEXTAREA_PADDING = 4;
const TEXTAREA_LINE_HEIGHT = 24;
const ActionBar = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
`;
const SyntaxOverlay = (0, styled_1.default)('div') `
  ${input_1.inputStyles};
  width: 100%;
  height: ${TEXTAREA_LINE_HEIGHT}px;
  background-color: red;
  opacity: 0.1;
  pointer-events: none;
  position: absolute;
  top: ${({ line }) => TEXTAREA_PADDING + line * 24}px;
`;
const SaveButton = (0, styled_1.default)('div') `
  text-align: end;
  padding-top: 10px;
`;
const StyledTextArea = (0, styled_1.default)(react_autosize_textarea_1.default) `
  ${p => (0, input_1.inputStyles)(p)};
  min-height: 140px;
  overflow: auto;
  outline: 0;
  width: 100%;
  resize: none;
  margin: 0;
  font-family: ${p => p.theme.text.familyMono};
  word-break: break-all;
  white-space: pre-wrap;
  padding-top: ${TEXTAREA_PADDING}px;
  line-height: ${TEXTAREA_LINE_HEIGHT}px;
`;
const InvalidOwners = (0, styled_1.default)('div') `
  color: ${p => p.theme.error};
  font-weight: bold;
  margin-top: 12px;
`;
exports.default = OwnerInput;
//# sourceMappingURL=ownerInput.jsx.map