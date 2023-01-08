
import * as React from 'react';
import { BarChart } from '../../components/barchart';
import { FileUpload } from '../../components/fileUpload';
import { LineChart } from '../../components/linechart';

export function HomePage() {
  return (
  <>
    <h1 className='text-3xl font-bold underline'>HomePage</h1>
    <h2>File upload</h2>
    <FileUpload />
    <h2>Linechart</h2>
    <LineChart />
    <h2>BarChart</h2>
    <BarChart />
  </>
  );
}