Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const locale_1 = require("app/locale");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const filterThreadInfo_1 = (0, tslib_1.__importDefault)(require("./filterThreadInfo"));
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const option_1 = (0, tslib_1.__importDefault)(require("./option"));
const selectedOption_1 = (0, tslib_1.__importDefault)(require("./selectedOption"));
const DROPDOWN_MAX_HEIGHT = 400;
const ThreadSelector = ({ threads, event, exception, activeThread, onChange }) => {
    const getDropDownItem = (thread) => {
        const { label, filename, crashedInfo } = (0, filterThreadInfo_1.default)(event, thread, exception);
        const threadInfo = { label, filename };
        return {
            value: `#${thread.id}: ${thread.name} ${label} ${filename}`,
            threadInfo,
            thread,
            label: (<option_1.default id={thread.id} details={threadInfo} name={thread.name} crashed={thread.crashed} crashedInfo={crashedInfo}/>),
        };
    };
    const getItems = () => {
        const [crashed, notCrashed] = (0, partition_1.default)(threads, thread => !!(thread === null || thread === void 0 ? void 0 : thread.crashed));
        return [...crashed, ...notCrashed].map(getDropDownItem);
    };
    const handleChange = (thread) => {
        if (onChange) {
            onChange(thread);
        }
    };
    return (<StyledDropdownAutoComplete items={getItems()} onSelect={item => {
            handleChange(item.thread);
        }} maxHeight={DROPDOWN_MAX_HEIGHT} searchPlaceholder={(0, locale_1.t)('Filter Threads')} emptyMessage={(0, locale_1.t)('You have no threads')} noResultsMessage={(0, locale_1.t)('No threads found')} menuHeader={<header_1.default />} closeOnSelect emptyHidesInput>
      {({ isOpen, selectedItem }) => (<StyledDropdownButton size="small" isOpen={isOpen} align="left">
          {selectedItem ? (<selectedOption_1.default id={selectedItem.thread.id} details={selectedItem.threadInfo}/>) : (<selectedOption_1.default id={activeThread.id} details={(0, filterThreadInfo_1.default)(event, activeThread, exception)}/>)}
        </StyledDropdownButton>)}
    </StyledDropdownAutoComplete>);
};
exports.default = ThreadSelector;
const StyledDropdownAutoComplete = (0, styled_1.default)(dropdownAutoComplete_1.default) `
  width: 100%;
  min-width: 300px;
  @media (min-width: ${theme_1.default.breakpoints[0]}) {
    width: 500px;
  }
  @media (max-width: ${p => p.theme.breakpoints[2]}) {
    top: calc(100% - 2px);
  }
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  > *:first-child {
    grid-template-columns: 1fr 15px;
  }
  width: 100%;
  min-width: 150px;
  @media (min-width: ${props => props.theme.breakpoints[3]}) {
    max-width: 420px;
  }
`;
//# sourceMappingURL=index.jsx.map