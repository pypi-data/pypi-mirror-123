Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectField"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const memberListStore_1 = (0, tslib_1.__importDefault)(require("app/stores/memberListStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const selectOwners_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectOwnership/selectOwners"));
const initialState = {
    text: '',
    tagName: '',
    type: 'path',
    owners: [],
    isValid: false,
};
function getMatchPlaceholder(type) {
    switch (type) {
        case 'path':
            return 'src/example/*';
        case 'url':
            return 'https://example.com/settings/*';
        case 'tag':
            return 'tag-value';
        default:
            return '';
    }
}
class RuleBuilder extends React.Component {
    constructor() {
        super(...arguments);
        this.state = initialState;
        this.checkIsValid = () => {
            this.setState(state => ({
                isValid: !!state.text && state.owners && !!state.owners.length,
            }));
        };
        this.handleTypeChange = (val) => {
            this.setState({ type: val }); // TODO(ts): Add select value type as generic to select controls
            this.checkIsValid();
        };
        this.handleTagNameChangeValue = (e) => {
            this.setState({ tagName: e.target.value }, this.checkIsValid);
        };
        this.handleChangeValue = (e) => {
            this.setState({ text: e.target.value });
            this.checkIsValid();
        };
        this.handleChangeOwners = (owners) => {
            this.setState({ owners });
            this.checkIsValid();
        };
        this.handleAddRule = () => {
            const { type, text, tagName, owners, isValid } = this.state;
            if (!isValid) {
                (0, indicator_1.addErrorMessage)('A rule needs a type, a value, and one or more issue owners.');
                return;
            }
            const ownerText = owners
                .map(owner => {
                var _a;
                return owner.actor.type === 'team'
                    ? `#${owner.actor.name}`
                    : (_a = memberListStore_1.default.getById(owner.actor.id)) === null || _a === void 0 ? void 0 : _a.email;
            })
                .join(' ');
            const quotedText = text.match(/\s/) ? `"${text}"` : text;
            const rule = `${type === 'tag' ? `tags.${tagName}` : type}:${quotedText} ${ownerText}`;
            this.props.onAddRule(rule);
            this.setState(initialState);
        };
        this.handleSelectCandidate = (text, type) => {
            this.setState({ text, type });
            this.checkIsValid();
        };
    }
    render() {
        const { urls, paths, disabled, project, organization } = this.props;
        const { type, text, tagName, owners, isValid } = this.state;
        return (<React.Fragment>
        {(paths || urls) && (<Candidates>
            {paths &&
                    paths.map(v => (<RuleCandidate key={v} onClick={() => this.handleSelectCandidate(v, 'path')}>
                  <StyledIconAdd isCircled/>
                  <StyledTextOverflow>{v}</StyledTextOverflow>
                  <tag_1.default>{(0, locale_1.t)('Path')}</tag_1.default>
                </RuleCandidate>))}
            {urls &&
                    urls.map(v => (<RuleCandidate key={v} onClick={() => this.handleSelectCandidate(v, 'url')}>
                  <StyledIconAdd isCircled/>
                  <StyledTextOverflow>{v}</StyledTextOverflow>
                  <tag_1.default>{(0, locale_1.t)('URL')}</tag_1.default>
                </RuleCandidate>))}
          </Candidates>)}
        <BuilderBar>
          <BuilderSelect name="select-type" value={type} onChange={this.handleTypeChange} options={[
                { value: 'path', label: (0, locale_1.t)('Path') },
                { value: 'tag', label: (0, locale_1.t)('Tag') },
                { value: 'url', label: (0, locale_1.t)('URL') },
            ]} style={{ width: 140 }} clearable={false} disabled={disabled}/>
          {type === 'tag' && (<BuilderTagNameInput value={tagName} onChange={this.handleTagNameChangeValue} disabled={disabled} placeholder="tag-name"/>)}
          <BuilderInput value={text} onChange={this.handleChangeValue} disabled={disabled} placeholder={getMatchPlaceholder(type)}/>
          <Divider direction="right"/>
          <SelectOwnersWrapper>
            <selectOwners_1.default organization={organization} project={project} value={owners} onChange={this.handleChangeOwners} disabled={disabled}/>
          </SelectOwnersWrapper>

          <AddButton priority="primary" disabled={!isValid} onClick={this.handleAddRule} icon={<icons_1.IconAdd isCircled/>} size="small"/>
        </BuilderBar>
      </React.Fragment>);
    }
}
const Candidates = (0, styled_1.default)('div') `
  margin-bottom: 10px;
`;
const StyledTextOverflow = (0, styled_1.default)(textOverflow_1.default) `
  flex: 1;
`;
const RuleCandidate = (0, styled_1.default)('div') `
  font-family: ${p => p.theme.text.familyMono};
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius};
  background-color: ${p => p.theme.background};
  padding: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(0.5)};
  margin-bottom: ${(0, space_1.default)(0.5)};
  cursor: pointer;
  overflow: hidden;
  display: flex;
  align-items: center;
`;
const StyledIconAdd = (0, styled_1.default)(icons_1.IconAdd) `
  color: ${p => p.theme.border};
  margin-right: 5px;
  flex-shrink: 0;
`;
const BuilderBar = (0, styled_1.default)('div') `
  display: flex;
  height: 40px;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(2)};
`;
const BuilderSelect = (0, styled_1.default)(selectField_1.default) `
  margin-right: ${(0, space_1.default)(1.5)};
  width: 50px;
  flex-shrink: 0;
`;
const BuilderInput = (0, styled_1.default)(input_1.default) `
  padding: ${(0, space_1.default)(1)};
  line-height: 19px;
  margin-right: ${(0, space_1.default)(0.5)};
`;
const BuilderTagNameInput = (0, styled_1.default)(input_1.default) `
  padding: ${(0, space_1.default)(1)};
  line-height: 19px;
  margin-right: ${(0, space_1.default)(0.5)};
  width: 200px;
`;
const Divider = (0, styled_1.default)(icons_1.IconChevron) `
  color: ${p => p.theme.border};
  flex-shrink: 0;
  margin-right: 5px;
`;
const SelectOwnersWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-right: ${(0, space_1.default)(1)};
`;
const AddButton = (0, styled_1.default)(button_1.default) `
  padding: ${(0, space_1.default)(0.5)}; /* this sizes the button up to align with the inputs */
`;
exports.default = RuleBuilder;
//# sourceMappingURL=ruleBuilder.jsx.map