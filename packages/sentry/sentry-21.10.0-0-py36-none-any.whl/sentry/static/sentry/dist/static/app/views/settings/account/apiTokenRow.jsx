Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
function ApiTokenRow({ token, onRemove }) {
    return (<StyledPanelItem>
      <Controls>
        <InputWrapper>
          <textCopyInput_1.default>
            {(0, getDynamicText_1.default)({ value: token.token, fixed: 'CI_AUTH_TOKEN' })}
          </textCopyInput_1.default>
        </InputWrapper>
        <button_1.default size="small" onClick={() => onRemove(token)} icon={<icons_1.IconSubtract isCircled size="xs"/>}>
          {(0, locale_1.t)('Remove')}
        </button_1.default>
      </Controls>

      <Details>
        <ScopesWrapper>
          <Heading>{(0, locale_1.t)('Scopes')}</Heading>
          <ScopeList>{token.scopes.join(', ')}</ScopeList>
        </ScopesWrapper>
        <div>
          <Heading>{(0, locale_1.t)('Created')}</Heading>
          <Time>
            <dateTime_1.default date={(0, getDynamicText_1.default)({
            value: token.dateCreated,
            fixed: new Date(1508208080000), // National Pasta Day
        })}/>
          </Time>
        </div>
      </Details>
    </StyledPanelItem>);
}
const StyledPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  flex-direction: column;
  padding: ${(0, space_1.default)(2)};
`;
const Controls = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const InputWrapper = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeRelativeSmall};
  flex: 1;
  margin-right: ${(0, space_1.default)(1)};
`;
const Details = (0, styled_1.default)('div') `
  display: flex;
  margin-top: ${(0, space_1.default)(1)};
`;
const ScopesWrapper = (0, styled_1.default)('div') `
  flex: 1;
`;
const ScopeList = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeRelativeSmall};
  line-height: 1.4;
`;
const Time = (0, styled_1.default)('time') `
  font-size: ${p => p.theme.fontSizeRelativeSmall};
  line-height: 1.4;
`;
const Heading = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  text-transform: uppercase;
  color: ${p => p.theme.subText};
  margin-bottom: ${(0, space_1.default)(1)};
`;
exports.default = ApiTokenRow;
//# sourceMappingURL=apiTokenRow.jsx.map