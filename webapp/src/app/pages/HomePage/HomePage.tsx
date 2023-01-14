import axios from 'axios';
import { useEffect, useState } from 'react';
import { BarChart } from '../../components/barchart';
import { FileUpload } from '../../components/fileUpload';
import { LineChart } from '../../components/linechart';


interface transaction {
  date: string,
  currency_sold: string,
  amount_sold: number,
  price_sold: number,
  currency_bought: string,
  amount_bought: number
  price_bought: number
}

interface TransactionData {
  transactions: transaction[],
  amounts: any, //TODO: Fix
  transaction_profits: number[],
  transaction_currency_profits: any,
  currency_profits: any
}

export function HomePage() {

  const [transactionData, setTransactionData] = useState<TransactionData>()
  const [prices, setPrices] = useState<any>()
  const [errorMessage, setErrorMessage] = useState<string>()

  useEffect(() => {
    axios.get("http://localhost:8000/profits")
    .then((res) => {
      setTransactionData(res.data)
    })
    .catch((err) => {
      setErrorMessage(err.message)
    })
  }, [])
  
  useEffect(() => {
    axios.get("http://localhost:8000/prices")
    .then((res) => {
      setPrices(res.data)
    })
    .catch((err) => {
      setErrorMessage(err.message)
    })
  }, [])


  console.log(transactionData)

  return (
  <>
    <h1 className='text-3xl font-bold'>Total profit per currency</h1>
    {
      transactionData &&
      <BarChart labels={Object.keys(transactionData?.currency_profits)} values={transactionData.currency_profits}/>
    }
    
    <h1 className='text-3xl font-bold'>Amounts per currency</h1>
    {
      transactionData &&
      <BarChart labels={Object.keys(transactionData?.amounts.total)} values={transactionData.amounts.total}/>
    }
    <h1 className='text-3xl font-bold'>Prices</h1>
    {
      prices &&
      <LineChart labels={prices.dates} values={prices.data}/>
    }
    {errorMessage ? errorMessage : ""}
  </>
  );
}