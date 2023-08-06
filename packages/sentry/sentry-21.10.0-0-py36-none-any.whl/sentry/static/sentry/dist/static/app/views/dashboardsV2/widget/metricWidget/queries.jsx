Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const groupByField_1 = (0, tslib_1.__importDefault)(require("./groupByField"));
const metricSelectField_1 = (0, tslib_1.__importDefault)(require("./metricSelectField"));
function Queries({ metricMetas, metricTags, queries, onRemoveQuery, onAddQuery, onChangeQuery, }) {
    function handleFieldChange(queryIndex, field) {
        const widgetQuery = queries[queryIndex];
        return function handleChange(value) {
            const newQuery = Object.assign(Object.assign({}, widgetQuery), { [field]: value });
            onChangeQuery(queryIndex, newQuery);
        };
    }
    return (<Wrapper>
      {queries.map((query, queryIndex) => {
            return (<Fields displayDeleteButton={queries.length > 1} key={queryIndex}>
            <metricSelectField_1.default metricMetas={metricMetas} metricMeta={query.metricMeta} aggregation={query.aggregation} onChange={(field, value) => handleFieldChange(queryIndex, field)(value)}/>
            <groupByField_1.default metricTags={metricTags} groupBy={query.groupBy} onChange={v => handleFieldChange(queryIndex, 'groupBy')(v)}/>
            <input_1.default type="text" name="legend" value={query.legend} placeholder={(0, locale_1.t)('Legend Alias')} onChange={event => handleFieldChange(queryIndex, 'legend')(event.target.value)} required/>
            {queries.length > 1 && (<react_1.Fragment>
                <ButtonDeleteWrapper>
                  <button_1.default onClick={() => {
                        onRemoveQuery(queryIndex);
                    }} size="small">
                    {(0, locale_1.t)('Delete Query')}
                  </button_1.default>
                </ButtonDeleteWrapper>
                <IconDeleteWrapper onClick={() => {
                        onRemoveQuery(queryIndex);
                    }}>
                  <icons_1.IconDelete aria-label={(0, locale_1.t)('Delete Query')}/>
                </IconDeleteWrapper>
              </react_1.Fragment>)}
          </Fields>);
        })}
      <div>
        <button_1.default size="small" icon={<icons_1.IconAdd isCircled/>} onClick={onAddQuery}>
          {(0, locale_1.t)('Add query')}
        </button_1.default>
      </div>
    </Wrapper>);
}
exports.default = Queries;
const IconDeleteWrapper = (0, styled_1.default)('div') `
  height: 40px;
  cursor: pointer;
  display: none;

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    display: flex;
    align-items: center;
  }
`;
const Fields = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    grid-template-columns: ${p => p.displayDeleteButton ? '1.3fr 1fr 0.5fr max-content' : '1.3fr 1fr 0.5fr'};
    grid-gap: ${(0, space_1.default)(1)};
    align-items: center;
  }
`;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
  @media (max-width: ${p => p.theme.breakpoints[3]}) {
    ${Fields} {
      :not(:first-child) {
        border-top: 1px solid ${p => p.theme.border};
        padding-top: ${(0, space_1.default)(2)};
      }
    }
  }
`;
const ButtonDeleteWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    display: none;
  }
`;
//# sourceMappingURL=queries.jsx.map