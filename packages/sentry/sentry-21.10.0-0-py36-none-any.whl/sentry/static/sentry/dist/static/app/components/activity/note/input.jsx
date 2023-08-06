Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_mentions_1 = require("react-mentions");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const text_1 = (0, tslib_1.__importDefault)(require("app/styles/text"));
const marked_1 = (0, tslib_1.__importDefault)(require("app/utils/marked"));
const mentionables_1 = (0, tslib_1.__importDefault)(require("./mentionables"));
const mentionStyle_1 = (0, tslib_1.__importDefault)(require("./mentionStyle"));
const defaultProps = {
    placeholder: (0, locale_1.t)('Add a comment.\nTag users with @, or teams with #'),
    minHeight: 140,
    busy: false,
};
class NoteInputComponent extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            preview: false,
            value: this.props.text || '',
            memberMentions: [],
            teamMentions: [],
        };
        this.handleToggleEdit = () => {
            this.setState({ preview: false });
        };
        this.handleTogglePreview = () => {
            this.setState({ preview: true });
        };
        this.handleSubmit = (e) => {
            e.preventDefault();
            this.submitForm();
        };
        this.handleChange = e => {
            this.setState({ value: e.target.value });
            if (this.props.onChange) {
                this.props.onChange(e, { updating: !!this.props.modelId });
            }
        };
        this.handleKeyDown = e => {
            // Auto submit the form on [meta,ctrl] + Enter
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey) && this.canSubmit) {
                this.submitForm();
            }
        };
        this.handleCancel = (e) => {
            e.preventDefault();
            this.finish();
        };
        this.handleAddMember = (id, display) => {
            this.setState(({ memberMentions }) => ({
                memberMentions: [...memberMentions, [`${id}`, display]],
            }));
        };
        this.handleAddTeam = (id, display) => {
            this.setState(({ teamMentions }) => ({
                teamMentions: [...teamMentions, [`${id}`, display]],
            }));
        };
    }
    get canSubmit() {
        return this.state.value.trim() !== '';
    }
    cleanMarkdown(text) {
        return text
            .replace(/\[sentry\.strip:member\]/g, '@')
            .replace(/\[sentry\.strip:team\]/g, '');
    }
    submitForm() {
        if (!!this.props.modelId) {
            this.update();
            return;
        }
        this.create();
    }
    create() {
        const { onCreate } = this.props;
        if (onCreate) {
            onCreate({
                text: this.cleanMarkdown(this.state.value),
                mentions: this.finalizeMentions(),
            });
        }
    }
    update() {
        const { onUpdate } = this.props;
        if (onUpdate) {
            onUpdate({
                text: this.cleanMarkdown(this.state.value),
                mentions: this.finalizeMentions(),
            });
        }
    }
    finish() {
        this.props.onEditFinish && this.props.onEditFinish();
    }
    finalizeMentions() {
        const { memberMentions, teamMentions } = this.state;
        // each mention looks like [id, display]
        return [...memberMentions, ...teamMentions]
            .filter(mention => this.state.value.indexOf(mention[1]) !== -1)
            .map(mention => mention[0]);
    }
    render() {
        const { preview, value } = this.state;
        const { modelId, busy, placeholder, minHeight, errorJSON, memberList, teams, theme } = this.props;
        const existingItem = !!modelId;
        const btnText = existingItem ? (0, locale_1.t)('Save Comment') : (0, locale_1.t)('Post Comment');
        const errorMessage = (errorJSON &&
            (typeof errorJSON.detail === 'string'
                ? errorJSON.detail
                : (errorJSON.detail && errorJSON.detail.message) ||
                    (0, locale_1.t)('Unable to post comment'))) ||
            null;
        return (<NoteInputForm data-test-id="note-input-form" noValidate onSubmit={this.handleSubmit}>
        <NoteInputNavTabs>
          <NoteInputNavTab className={!preview ? 'active' : ''}>
            <NoteInputNavTabLink onClick={this.handleToggleEdit}>
              {existingItem ? (0, locale_1.t)('Edit') : (0, locale_1.t)('Write')}
            </NoteInputNavTabLink>
          </NoteInputNavTab>
          <NoteInputNavTab className={preview ? 'active' : ''}>
            <NoteInputNavTabLink onClick={this.handleTogglePreview}>
              {(0, locale_1.t)('Preview')}
            </NoteInputNavTabLink>
          </NoteInputNavTab>
          <MarkdownTab>
            <icons_1.IconMarkdown />
            <MarkdownSupported>{(0, locale_1.t)('Markdown supported')}</MarkdownSupported>
          </MarkdownTab>
        </NoteInputNavTabs>

        <NoteInputBody>
          {preview ? (<NotePreview minHeight={minHeight} dangerouslySetInnerHTML={{ __html: (0, marked_1.default)(this.cleanMarkdown(value)) }}/>) : (<react_mentions_1.MentionsInput style={(0, mentionStyle_1.default)({ theme, minHeight })} placeholder={placeholder} onChange={this.handleChange} onKeyDown={this.handleKeyDown} value={value} required autoFocus>
              <react_mentions_1.Mention trigger="@" data={memberList} onAdd={this.handleAddMember} displayTransform={(_id, display) => `@${display}`} markup="**[sentry.strip:member]__display__**" appendSpaceOnAdd/>
              <react_mentions_1.Mention trigger="#" data={teams} onAdd={this.handleAddTeam} markup="**[sentry.strip:team]__display__**" appendSpaceOnAdd/>
            </react_mentions_1.MentionsInput>)}
        </NoteInputBody>

        <Footer>
          <div>{errorMessage && <ErrorMessage>{errorMessage}</ErrorMessage>}</div>
          <div>
            {existingItem && (<FooterButton priority="danger" type="button" onClick={this.handleCancel}>
                {(0, locale_1.t)('Cancel')}
              </FooterButton>)}
            <FooterButton error={errorMessage} type="submit" disabled={busy || !this.canSubmit}>
              {btnText}
            </FooterButton>
          </div>
        </Footer>
      </NoteInputForm>);
    }
}
const NoteInput = (0, react_1.withTheme)(NoteInputComponent);
class NoteInputContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.renderInput = ({ members, teams }) => {
            const _a = this.props, { projectSlugs: _ } = _a, props = (0, tslib_1.__rest)(_a, ["projectSlugs"]);
            return <NoteInput memberList={members} teams={teams} {...props}/>;
        };
    }
    render() {
        const { projectSlugs } = this.props;
        const me = configStore_1.default.get('user');
        return (<mentionables_1.default me={me} projectSlugs={projectSlugs}>
        {this.renderInput}
      </mentionables_1.default>);
    }
}
NoteInputContainer.defaultProps = defaultProps;
exports.default = NoteInputContainer;
// This styles both the note preview and the note editor input
const getNotePreviewCss = (p) => {
    const { minHeight, padding, overflow, border } = (0, mentionStyle_1.default)(p)['&multiLine'].input;
    return `
  max-height: 1000px;
  max-width: 100%;
  ${(minHeight && `min-height: ${minHeight}px`) || ''};
  padding: ${padding};
  overflow: ${overflow};
  border: ${border};
`;
};
const getNoteInputErrorStyles = (p) => {
    if (!p.error) {
        return '';
    }
    return `
  color: ${p.theme.error};
  margin: -1px;
  border: 1px solid ${p.theme.error};
  border-radius: ${p.theme.borderRadius};

    &:before {
      display: block;
      content: '';
      width: 0;
      height: 0;
      border-top: 7px solid transparent;
      border-bottom: 7px solid transparent;
      border-right: 7px solid ${p.theme.red300};
      position: absolute;
      left: -7px;
      top: 12px;
    }

    &:after {
      display: block;
      content: '';
      width: 0;
      height: 0;
      border-top: 6px solid transparent;
      border-bottom: 6px solid transparent;
      border-right: 6px solid #fff;
      position: absolute;
      left: -5px;
      top: 12px;
    }
  `;
};
const NoteInputForm = (0, styled_1.default)('form') `
  font-size: 15px;
  line-height: 22px;
  transition: padding 0.2s ease-in-out;

  ${p => getNoteInputErrorStyles(p)}
`;
const NoteInputBody = (0, styled_1.default)('div') `
  ${text_1.default}
`;
const Footer = (0, styled_1.default)('div') `
  display: flex;
  border-top: 1px solid ${p => p.theme.border};
  justify-content: space-between;
  transition: opacity 0.2s ease-in-out;
  padding-left: ${(0, space_1.default)(1.5)};
`;
const FooterButton = (0, styled_1.default)(button_1.default) `
  font-size: 13px;
  margin: -1px -1px -1px;
  border-radius: 0 0 ${p => p.theme.borderRadius};

  ${p => p.error &&
    `
  &, &:active, &:focus, &:hover {
  border-bottom-color: ${p.theme.error};
  border-right-color: ${p.theme.error};
  }
  `}
`;
const ErrorMessage = (0, styled_1.default)('span') `
  display: flex;
  align-items: center;
  height: 100%;
  color: ${p => p.theme.error};
  font-size: 0.9em;
`;
const NoteInputNavTabs = (0, styled_1.default)(navTabs_1.default) `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)} 0;
  border-bottom: 1px solid ${p => p.theme.border};
  margin-bottom: 0;
`;
const NoteInputNavTab = (0, styled_1.default)('li') `
  margin-right: 13px;
`;
const NoteInputNavTabLink = (0, styled_1.default)('a') `
  .nav-tabs > li > & {
    font-size: 15px;
    padding-bottom: 5px;
  }
`;
const MarkdownTab = (0, styled_1.default)(NoteInputNavTab) `
  .nav-tabs > & {
    display: flex;
    align-items: center;
    margin-right: 0;
    color: ${p => p.theme.subText};

    float: right;
  }
`;
const MarkdownSupported = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(0.5)};
  font-size: 14px;
`;
const NotePreview = (0, styled_1.default)('div') `
  ${p => getNotePreviewCss(p)};
  padding-bottom: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=input.jsx.map