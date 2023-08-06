Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const layout_1 = (0, tslib_1.__importDefault)(require("../layout"));
const utils_1 = require("../utils");
const processings_1 = (0, tslib_1.__importDefault)(require("./processings"));
const status_1 = (0, tslib_1.__importDefault)(require("./status"));
function DebugImage({ image, onOpenImageDetailsModal, style }) {
    const { unwind_status, debug_status, debug_file, debug_id, code_file, code_id, status } = image;
    const codeFilename = (0, utils_1.getFileName)(code_file);
    const debugFilename = (0, utils_1.getFileName)(debug_file);
    const imageAddress = (0, utils_1.getImageAddress)(image);
    return (<Wrapper style={style}>
      <StatusColumn>
        <status_1.default status={status}/>
      </StatusColumn>
      <ImageColumn>
        <div>
          {codeFilename && (<FileName>
              <tooltip_1.default title={code_file}>{codeFilename}</tooltip_1.default>
            </FileName>)}
          {codeFilename !== debugFilename && debugFilename && (<CodeFilename>{`(${debugFilename})`}</CodeFilename>)}
        </div>
        {imageAddress && <ImageAddress>{imageAddress}</ImageAddress>}
      </ImageColumn>
      <Column>
        {unwind_status || debug_status ? (<processings_1.default unwind_status={unwind_status} debug_status={debug_status}/>) : (<notAvailable_1.default />)}
      </Column>
      <DebugFilesColumn>
        <button_1.default size="xsmall" onClick={() => onOpenImageDetailsModal(code_id, debug_id)}>
          {(0, locale_1.t)('View')}
        </button_1.default>
      </DebugFilesColumn>
    </Wrapper>);
}
exports.default = DebugImage;
const Wrapper = (0, styled_1.default)('div') `
  :not(:last-child) {
    > * {
      border-bottom: 1px solid ${p => p.theme.border};
    }
  }
  ${p => (0, layout_1.default)(p.theme)};
`;
const Column = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)};
  display: flex;
  align-items: center;
`;
const StatusColumn = (0, styled_1.default)(Column) `
  max-width: 100%;
  overflow: hidden;
`;
const FileName = (0, styled_1.default)('span') `
  color: ${p => p.theme.textColor};
  font-family: ${p => p.theme.text.family};
  font-size: ${p => p.theme.fontSizeMedium};
  margin-right: ${(0, space_1.default)(0.5)};
  white-space: pre-wrap;
  word-break: break-all;
`;
const CodeFilename = (0, styled_1.default)('span') `
  color: ${p => p.theme.subText};
`;
const ImageColumn = (0, styled_1.default)(Column) `
  font-family: ${p => p.theme.text.familyMono};
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeSmall};
  overflow: hidden;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
`;
const ImageAddress = (0, styled_1.default)('div') `
  white-space: pre-wrap;
  word-break: break-word;
`;
const DebugFilesColumn = (0, styled_1.default)(Column) `
  justify-content: flex-end;
`;
//# sourceMappingURL=index.jsx.map