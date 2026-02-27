import pytest

from kis_client.domestic_stock.core.kis_domestic_stock_master_file_manager import \
    KoreaInvestmentSecuritiesDomesticStockMasterFileManager


@pytest.mark.asyncio
async def test_set_credentials():
    master_file_manager = KoreaInvestmentSecuritiesDomesticStockMasterFileManager()
    master_file_manager.synchronize()

    master_file_manager.kosfi_dataframe.to_excel('kospi_code.xlsx', index=False)
    master_file_manager.kosdaq_dataframe.to_excel('kosdaq_code.xlsx', index=False)

    assert master_file_manager.kosfi_dataframe is not None
    assert master_file_manager.kosdaq_dataframe is not None
    assert len(master_file_manager.kosfi_dataframe) > 0
    assert len(master_file_manager.kosdaq_dataframe) > 0

    print(master_file_manager.kosfi_dataframe.columns)
    assert len(master_file_manager.kosfi_dataframe[master_file_manager.kosfi_dataframe[("한글명")] == "삼성전자"]) == 1
    assert len(master_file_manager.kosfi_dataframe[master_file_manager.kosfi_dataframe[("단축코드")] == "005930"]) == 1

    print(master_file_manager.kosdaq_dataframe.columns)
    assert len(master_file_manager.kosdaq_dataframe[master_file_manager.kosdaq_dataframe[("한글명")] == "셀트리온제약"]) == 1
    assert len(master_file_manager.kosdaq_dataframe[master_file_manager.kosdaq_dataframe[("단축코드")] == "068760"]) == 1
