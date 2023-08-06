Object.defineProperty(exports, "__esModule", { value: true });
exports.AutoCompleteRoot = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const autoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/autoComplete"));
const dropdownBubble_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownBubble"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const autoCompleteFilter_1 = (0, tslib_1.__importDefault)(require("./autoCompleteFilter"));
const list_1 = (0, tslib_1.__importDefault)(require("./list"));
const Menu = (_a) => {
    var { maxHeight = 300, emptyMessage = (0, locale_1.t)('No items'), searchPlaceholder = (0, locale_1.t)('Filter search'), blendCorner = true, alignMenu = 'left', hideInput = false, busy = false, busyItemsStillVisible = false, menuWithArrow = false, disabled = false, itemSize, virtualizedHeight, virtualizedLabelHeight, menuProps, noResultsMessage, inputProps, children, rootClassName, className, emptyHidesInput, menuHeader, filterValue, items, menuFooter, style, onScroll, inputActions, onChange, onSelect, onOpen, onClose, css, closeOnSelect } = _a, props = (0, tslib_1.__rest)(_a, ["maxHeight", "emptyMessage", "searchPlaceholder", "blendCorner", "alignMenu", "hideInput", "busy", "busyItemsStillVisible", "menuWithArrow", "disabled", "itemSize", "virtualizedHeight", "virtualizedLabelHeight", "menuProps", "noResultsMessage", "inputProps", "children", "rootClassName", "className", "emptyHidesInput", "menuHeader", "filterValue", "items", "menuFooter", "style", "onScroll", "inputActions", "onChange", "onSelect", "onOpen", "onClose", "css", "closeOnSelect"]);
    return (<autoComplete_1.default onSelect={onSelect} inputIsActor={false} onOpen={onOpen} onClose={onClose} disabled={disabled} closeOnSelect={closeOnSelect} resetInputOnClose {...props}>
    {({ getActorProps, getRootProps, getInputProps, getMenuProps, getItemProps, inputValue, selectedItem, highlightedIndex, isOpen, actions, }) => {
            // This is the value to use to filter (default to value in filter input)
            const filterValueOrInput = filterValue !== null && filterValue !== void 0 ? filterValue : inputValue;
            // Can't search if there are no items
            const hasItems = !!(items === null || items === void 0 ? void 0 : items.length);
            // Only filter results if menu is open and there are items
            const autoCompleteResults = (isOpen && hasItems && (0, autoCompleteFilter_1.default)(items, filterValueOrInput)) || [];
            // Items are loading if null
            const itemsLoading = items === null;
            // Has filtered results
            const hasResults = !!autoCompleteResults.length;
            // No items to display
            const showNoItems = !busy && !filterValueOrInput && !hasItems;
            // Results mean there was an attempt to search
            const showNoResultsMessage = !busy && !busyItemsStillVisible && filterValueOrInput && !hasResults;
            // Hide the input when we have no items to filter, only if
            // emptyHidesInput is set to true.
            const showInput = !hideInput && (hasItems || !emptyHidesInput);
            // When virtualization is turned on, we need to pass in the number of
            // selecteable items for arrow-key limits
            const itemCount = virtualizedHeight
                ? autoCompleteResults.filter(i => !i.groupLabel).length
                : undefined;
            const renderedFooter = typeof menuFooter === 'function' ? menuFooter({ actions }) : menuFooter;
            return (<exports.AutoCompleteRoot {...getRootProps()} className={rootClassName} disabled={disabled}>
          {children({
                    getInputProps,
                    getActorProps,
                    actions,
                    isOpen,
                    selectedItem,
                })}
          {isOpen && (<BubbleWithMinWidth className={className} {...getMenuProps(Object.assign(Object.assign({}, menuProps), { itemCount }))} style={style} css={css} blendCorner={blendCorner} alignMenu={alignMenu} menuWithArrow={menuWithArrow}>
              {itemsLoading && <loadingIndicator_1.default mini/>}
              {showInput && (<InputWrapper>
                  <StyledInput autoFocus placeholder={searchPlaceholder} {...getInputProps(Object.assign(Object.assign({}, inputProps), { onChange }))}/>
                  <InputLoadingWrapper>
                    {(busy || busyItemsStillVisible) && (<loadingIndicator_1.default size={16} mini/>)}
                  </InputLoadingWrapper>
                  {inputActions}
                </InputWrapper>)}
              <div>
                {menuHeader && <LabelWithPadding>{menuHeader}</LabelWithPadding>}
                <ItemList data-test-id="autocomplete-list" maxHeight={maxHeight}>
                  {showNoItems && <EmptyMessage>{emptyMessage}</EmptyMessage>}
                  {showNoResultsMessage && (<EmptyMessage>
                      {noResultsMessage !== null && noResultsMessage !== void 0 ? noResultsMessage : `${emptyMessage} ${(0, locale_1.t)('found')}`}
                    </EmptyMessage>)}
                  {busy && (<BusyMessage>
                      <EmptyMessage>{(0, locale_1.t)('Searching\u2026')}</EmptyMessage>
                    </BusyMessage>)}
                  {!busy && (<list_1.default items={autoCompleteResults} maxHeight={maxHeight} highlightedIndex={highlightedIndex} inputValue={inputValue} onScroll={onScroll} getItemProps={getItemProps} virtualizedLabelHeight={virtualizedLabelHeight} virtualizedHeight={virtualizedHeight} itemSize={itemSize}/>)}
                </ItemList>
                {renderedFooter && <LabelWithPadding>{renderedFooter}</LabelWithPadding>}
              </div>
            </BubbleWithMinWidth>)}
        </exports.AutoCompleteRoot>);
        }}
  </autoComplete_1.default>);
};
exports.default = Menu;
const StyledInput = (0, styled_1.default)(input_1.default) `
  flex: 1;
  border: 1px solid transparent;
  &,
  &:focus,
  &:active,
  &:hover {
    border: 0;
    box-shadow: none;
    font-size: 13px;
    padding: ${(0, space_1.default)(1)};
    font-weight: normal;
    color: ${p => p.theme.gray300};
  }
`;
const InputLoadingWrapper = (0, styled_1.default)('div') `
  display: flex;
  background: ${p => p.theme.background};
  align-items: center;
  flex-shrink: 0;
  width: 30px;
  .loading.mini {
    height: 16px;
    margin: 0;
  }
`;
const EmptyMessage = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray200};
  padding: ${(0, space_1.default)(2)};
  text-align: center;
  text-transform: none;
`;
exports.AutoCompleteRoot = (0, styled_1.default)((_a) => {
    var { isOpen: _isOpen } = _a, props = (0, tslib_1.__rest)(_a, ["isOpen"]);
    return (<div {...props}/>);
}) `
  position: relative;
  display: inline-block;
  ${p => p.disabled && 'pointer-events: none;'}
`;
const BubbleWithMinWidth = (0, styled_1.default)(dropdownBubble_1.default) `
  min-width: 250px;
`;
const InputWrapper = (0, styled_1.default)('div') `
  display: flex;
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  border-radius: ${p => `${p.theme.borderRadius} ${p.theme.borderRadius} 0 0`};
  align-items: center;
`;
const LabelWithPadding = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.backgroundSecondary};
  border-bottom: 1px solid ${p => p.theme.innerBorder};
  border-width: 1px 0;
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  &:first-child {
    border-top: none;
  }
  &:last-child {
    border-bottom: none;
  }
  padding: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(1)};
`;
const ItemList = (0, styled_1.default)('div') `
  max-height: ${p => `${p.maxHeight}px`};
  overflow-y: auto;
`;
const BusyMessage = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  padding: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=menu.jsx.map