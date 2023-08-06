Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const iconDelete_1 = require("app/icons/iconDelete");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dynamicSampling_1 = require("app/types/dynamicSampling");
const fieldRequiredBadge_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/fieldRequiredBadge"));
const textareaField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textareaField"));
const utils_1 = require("../utils");
const autoComplete_1 = (0, tslib_1.__importDefault)(require("./autoComplete"));
const legacyBrowsers_1 = (0, tslib_1.__importDefault)(require("./legacyBrowsers"));
const utils_2 = require("./utils");
function Conditions({ conditions, orgSlug, projectId, onDelete, onChange }) {
    return (<react_1.Fragment>
      {conditions.map(({ category, match, legacyBrowsers }, index) => {
            const displayLegacyBrowsers = category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER;
            const isBooleanField = category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS ||
                category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST ||
                category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS ||
                displayLegacyBrowsers;
            const isAutoCompleteField = category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_ENVIRONMENT ||
                category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE ||
                category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_TRANSACTION ||
                category === dynamicSampling_1.DynamicSamplingInnerName.TRACE_ENVIRONMENT ||
                category === dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE ||
                category === dynamicSampling_1.DynamicSamplingInnerName.TRACE_TRANSACTION;
            return (<ConditionWrapper key={index}>
            <LeftCell>
              <span>
                {(0, utils_1.getInnerNameLabel)(category)}
                <fieldRequiredBadge_1.default />
              </span>
            </LeftCell>
            <CenterCell>
              {!isBooleanField &&
                    (isAutoCompleteField ? (<autoComplete_1.default category={category} orgSlug={orgSlug} projectId={projectId} value={match} onChange={value => onChange(index, 'match', value)}/>) : (<StyledTextareaField name="match" value={match} onChange={value => onChange(index, 'match', value)} placeholder={(0, utils_2.getMatchFieldPlaceholder)(category)} inline={false} rows={1} autosize hideControlState flexibleControlStateSize required stacked/>))}
            </CenterCell>
            <RightCell>
              <button_1.default onClick={() => onDelete(index)} icon={<iconDelete_1.IconDelete />} label={(0, locale_1.t)('Delete Condition')}/>
            </RightCell>
            {displayLegacyBrowsers && (<legacyBrowsers_1.default selectedLegacyBrowsers={legacyBrowsers} onChange={value => {
                        onChange(index, 'legacyBrowsers', value);
                    }}/>)}
          </ConditionWrapper>);
        })}
    </react_1.Fragment>);
}
exports.default = Conditions;
const ConditionWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr minmax(0, 1fr);
  align-items: flex-start;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  :not(:last-child) {
    border-bottom: 1px solid ${p => p.theme.gray100};
  }

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 0.6fr minmax(0, 1fr) max-content;
  }
`;
const Cell = (0, styled_1.default)('div') `
  min-height: 40px;
  display: inline-flex;
  align-items: center;
`;
const LeftCell = (0, styled_1.default)(Cell) `
  padding-right: ${(0, space_1.default)(2)};
  line-height: 16px;
`;
const CenterCell = (0, styled_1.default)(Cell) `
  padding-top: ${(0, space_1.default)(1)};
  grid-column: 1/-1;
  grid-row: 2/2;
  ${p => !p.children && 'display: none'};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-column: auto;
    grid-row: auto;
    padding-top: 0;
  }
`;
const RightCell = (0, styled_1.default)(Cell) `
  justify-content: flex-end;
  padding-left: ${(0, space_1.default)(1)};
`;
const StyledTextareaField = (0, styled_1.default)(textareaField_1.default) `
  padding-bottom: 0;
  width: 100%;
`;
//# sourceMappingURL=conditions.jsx.map