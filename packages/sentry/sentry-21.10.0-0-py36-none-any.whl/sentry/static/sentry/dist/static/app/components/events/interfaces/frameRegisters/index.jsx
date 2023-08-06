Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const utils_2 = require("./utils");
const value_1 = (0, tslib_1.__importDefault)(require("./value"));
function FrameRegisters({ registers, deviceArch }) {
    // make sure that clicking on the registers does not actually do
    // anything on the containing element.
    const handlePreventToggling = (event) => {
        event.stopPropagation();
    };
    const sortedRegisters = (0, utils_2.getSortedRegisters)(registers, deviceArch);
    return (<Wrapper>
      <Heading>{(0, locale_1.t)('registers')}</Heading>
      <Registers>
        {sortedRegisters.map(([name, value]) => {
            if (!(0, utils_1.defined)(value)) {
                return null;
            }
            return (<Register key={name} onClick={handlePreventToggling}>
              <Name>{name}</Name>
              <value_1.default value={value} meta={(0, metaProxy_1.getMeta)(registers, name)}/>
            </Register>);
        })}
      </Registers>
    </Wrapper>);
}
const Wrapper = (0, styled_1.default)('div') `
  border-top: 1px solid ${p => p.theme.innerBorder};
  padding-top: 10px;
`;
const Registers = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
  margin-left: 125px;
  padding: ${(0, space_1.default)(0.25)} 0px;
`;
const Register = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(0.5)} 5px;
`;
const Heading = (0, styled_1.default)('strong') `
  font-weight: 600;
  font-size: 13px;
  width: 125px;
  max-width: 125px;
  word-wrap: break-word;
  padding: 10px 15px 10px 0;
  line-height: 1.4;
  float: left;
`;
const Name = (0, styled_1.default)('span') `
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  text-align: right;
  width: 4em;
`;
exports.default = FrameRegisters;
//# sourceMappingURL=index.jsx.map