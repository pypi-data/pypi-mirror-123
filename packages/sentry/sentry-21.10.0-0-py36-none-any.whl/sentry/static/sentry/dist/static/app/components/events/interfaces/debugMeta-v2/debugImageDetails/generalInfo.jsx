Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const processings_1 = (0, tslib_1.__importDefault)(require("../debugImage/processings"));
const utils_1 = require("../utils");
function GeneralInfo({ image }) {
    const { debug_id, debug_file, code_id, code_file, arch, unwind_status, debug_status } = image !== null && image !== void 0 ? image : {};
    const imageAddress = image ? (0, utils_1.getImageAddress)(image) : undefined;
    return (<Wrapper>
      <Label coloredBg>{(0, locale_1.t)('Address Range')}</Label>
      <Value coloredBg>{imageAddress !== null && imageAddress !== void 0 ? imageAddress : <notAvailable_1.default />}</Value>

      <Label>{(0, locale_1.t)('Debug ID')}</Label>
      <Value>{debug_id !== null && debug_id !== void 0 ? debug_id : <notAvailable_1.default />}</Value>

      <Label coloredBg>{(0, locale_1.t)('Debug File')}</Label>
      <Value coloredBg>{debug_file !== null && debug_file !== void 0 ? debug_file : <notAvailable_1.default />}</Value>

      <Label>{(0, locale_1.t)('Code ID')}</Label>
      <Value>{code_id !== null && code_id !== void 0 ? code_id : <notAvailable_1.default />}</Value>

      <Label coloredBg>{(0, locale_1.t)('Code File')}</Label>
      <Value coloredBg>{code_file !== null && code_file !== void 0 ? code_file : <notAvailable_1.default />}</Value>

      <Label>{(0, locale_1.t)('Architecture')}</Label>
      <Value>{arch !== null && arch !== void 0 ? arch : <notAvailable_1.default />}</Value>

      <Label coloredBg>{(0, locale_1.t)('Processing')}</Label>
      <Value coloredBg>
        {unwind_status || debug_status ? (<processings_1.default unwind_status={unwind_status} debug_status={debug_status}/>) : (<notAvailable_1.default />)}
      </Value>
    </Wrapper>);
}
exports.default = GeneralInfo;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
`;
const Label = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)} ${(0, space_1.default)(1)} ${(0, space_1.default)(1)};
  ${p => p.coloredBg && `background-color: ${p.theme.backgroundSecondary};`}
`;
const Value = (0, styled_1.default)(Label) `
  white-space: pre-wrap;
  word-break: break-all;
  color: ${p => p.theme.subText};
  padding: ${(0, space_1.default)(1)};
  font-family: ${p => p.theme.text.familyMono};
  ${p => p.coloredBg && `background-color: ${p.theme.backgroundSecondary};`}
`;
//# sourceMappingURL=generalInfo.jsx.map