Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const HealthStatsPeriod = ({ location, selection }) => {
    var _a;
    const activePeriod = location.query.healthStatsPeriod || types_1.HealthStatsPeriodOption.TWENTY_FOUR_HOURS;
    const { pathname, query } = location;
    return (<Wrapper>
      {selection.datetime.period !== types_1.HealthStatsPeriodOption.TWENTY_FOUR_HOURS && (<Period to={{
                pathname,
                query: Object.assign(Object.assign({}, query), { healthStatsPeriod: types_1.HealthStatsPeriodOption.TWENTY_FOUR_HOURS }),
            }} selected={activePeriod === types_1.HealthStatsPeriodOption.TWENTY_FOUR_HOURS}>
          {(0, locale_1.t)('24h')}
        </Period>)}

      <Period to={{
            pathname,
            query: Object.assign(Object.assign({}, query), { healthStatsPeriod: types_1.HealthStatsPeriodOption.AUTO }),
        }} selected={activePeriod === types_1.HealthStatsPeriodOption.AUTO}>
        {selection.datetime.start ? (0, locale_1.t)('Custom') : (_a = selection.datetime.period) !== null && _a !== void 0 ? _a : (0, locale_1.t)('14d')}
      </Period>
    </Wrapper>);
};
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-column-gap: ${(0, space_1.default)(0.75)};
  flex: 1;
  justify-content: flex-end;
  text-align: right;
  margin-left: ${(0, space_1.default)(0.5)};
`;
const Period = (0, styled_1.default)(link_1.default) `
  color: ${p => (p.selected ? p.theme.gray400 : p.theme.gray300)};

  &:hover,
  &:focus {
    color: ${p => (p.selected ? p.theme.gray400 : p.theme.gray300)};
  }
`;
exports.default = (0, withGlobalSelection_1.default)(HealthStatsPeriod);
//# sourceMappingURL=healthStatsPeriod.jsx.map