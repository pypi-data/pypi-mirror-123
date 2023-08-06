Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const styles_1 = require("./styles");
const Option = ({ id, details, name, crashed, crashedInfo }) => {
    const { label = `<${(0, locale_1.t)('unknown')}>`, filename = `<${(0, locale_1.t)('unknown')}>` } = details;
    const optionName = name || `<${(0, locale_1.t)('unknown')}>`;
    return (<styles_1.Grid>
      <styles_1.GridCell>
        <InnerCell>
          <tooltip_1.default title={`#${id}`} position="top">
            <textOverflow_1.default>{`#${id}`}</textOverflow_1.default>
          </tooltip_1.default>
        </InnerCell>
      </styles_1.GridCell>
      <styles_1.GridCell>
        <InnerCell isBold>
          <tooltip_1.default title={optionName} position="top">
            <textOverflow_1.default>{optionName}</textOverflow_1.default>
          </tooltip_1.default>
        </InnerCell>
      </styles_1.GridCell>
      <styles_1.GridCell>
        <InnerCell color="blue300">
          <tooltip_1.default title={label} position="top">
            <textOverflow_1.default>{label}</textOverflow_1.default>
          </tooltip_1.default>
        </InnerCell>
      </styles_1.GridCell>
      <styles_1.GridCell>
        <InnerCell color="purple300">
          <tooltip_1.default title={filename} position="top">
            <textOverflow_1.default>{filename}</textOverflow_1.default>
          </tooltip_1.default>
        </InnerCell>
      </styles_1.GridCell>
      <styles_1.GridCell>
        {crashed && (<InnerCell isCentered>
            {crashedInfo ? (<tooltip_1.default skipWrapper title={(0, locale_1.tct)('Errored with [crashedInfo]', {
                    crashedInfo: crashedInfo.values[0].type,
                })} position="top">
                <icons_1.IconFire color="red300"/>
              </tooltip_1.default>) : (<icons_1.IconFire color="red300"/>)}
          </InnerCell>)}
      </styles_1.GridCell>
    </styles_1.Grid>);
};
exports.default = Option;
const InnerCell = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: ${p => (p.isCentered ? 'center' : 'flex-start')};
  font-weight: ${p => (p.isBold ? 600 : 400)};
  ${p => p.color && `color: ${p.theme[p.color]}`}
`;
//# sourceMappingURL=option.jsx.map