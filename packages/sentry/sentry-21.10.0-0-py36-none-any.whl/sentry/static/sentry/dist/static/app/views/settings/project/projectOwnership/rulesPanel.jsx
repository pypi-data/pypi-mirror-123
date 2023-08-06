Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_autosize_textarea_1 = (0, tslib_1.__importDefault)(require("react-autosize-textarea"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const input_1 = require("app/styles/input");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function RulesPanel({ raw, dateUpdated, provider, repoName, type, placeholder, controls, ['data-test-id']: dataTestId, }) {
    function renderIcon() {
        switch (provider !== null && provider !== void 0 ? provider : '') {
            case 'github':
                return <icons_1.IconGithub size="md"/>;
            case 'gitlab':
                return <icons_1.IconGitlab size="md"/>;
            default:
                return <icons_1.IconSentry size="md"/>;
        }
    }
    function renderTitle() {
        switch (type) {
            case 'codeowners':
                return 'CODEOWNERS';
            case 'issueowners':
                return 'Ownership Rules';
            default:
                return null;
        }
    }
    return (<panels_1.Panel data-test-id={dataTestId}>
      <panels_1.PanelHeader>
        {[
            <Container key="title">
            {renderIcon()}
            <Title>{renderTitle()}</Title>
            {repoName && <Repository>{`- ${repoName}`}</Repository>}
            <featureBadge_1.default type="new"/>
          </Container>,
            <Container key="control">
            <SyncDate>
              {dateUpdated && `Last synced ${(0, moment_1.default)(dateUpdated).fromNow()}`}
            </SyncDate>
            <Controls>
              {(controls || []).map((c, n) => (<span key={n}> {c}</span>))}
            </Controls>
          </Container>,
        ]}
      </panels_1.PanelHeader>

      <panels_1.PanelBody>
        <InnerPanelBody>
          <StyledTextArea value={raw} spellCheck="false" autoComplete="off" autoCorrect="off" autoCapitalize="off" placeholder={placeholder}/>
        </InnerPanelBody>
      </panels_1.PanelBody>
    </panels_1.Panel>);
}
exports.default = RulesPanel;
const Container = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  text-transform: none;
`;
const Title = (0, styled_1.default)('div') `
  padding: 0 ${(0, space_1.default)(0.5)} 0 ${(0, space_1.default)(1)};
  font-size: initial;
`;
const Repository = (0, styled_1.default)('div') ``;
const InnerPanelBody = (0, styled_1.default)(panels_1.PanelBody) `
  height: auto;
`;
const StyledTextArea = (0, styled_1.default)(react_autosize_textarea_1.default) `
  ${p => (0, input_1.inputStyles)(p)};
  height: 350px !important;
  overflow: auto;
  outline: 0;
  width: 100%;
  resize: none;
  margin: 0;
  font-family: ${p => p.theme.text.familyMono};
  word-break: break-all;
  white-space: pre-wrap;
  line-height: ${(0, space_1.default)(3)};
  border: none;
  box-shadow: none;
  padding: ${(0, space_1.default)(2)};
  color: transparent;
  text-shadow: 0 0 0 #9386a0;

  &:hover,
  &:focus,
  &:active {
    border: none;
    box-shadow: none;
  }
`;
const SyncDate = (0, styled_1.default)('div') `
  padding: 0 ${(0, space_1.default)(1)};
  font-weight: normal;
`;
const Controls = (0, styled_1.default)('div') `
  display: grid;
  align-items: center;
  grid-gap: ${(0, space_1.default)(1)};
  grid-auto-flow: column;
  justify-content: flex-end;
`;
//# sourceMappingURL=rulesPanel.jsx.map