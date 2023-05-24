/// <reference types="vite/client" />
declare module 'APlayer' {
    export default class APlayer {
      constructor(options: APlayerOptions);
    }
    
    interface APlayerOptions {
      container: HTMLElement | null;
      audio: AudioInfo[];
      autoplay?: boolean;
      loop?: 'all' | 'one' | 'none';
      order?: 'list' | 'random';
      volume?: number;
      preload?: 'none' | 'metadata' | 'auto';
      listFolded?: boolean;
      listMaxHeight?: string;
      lrcType?: number;
      fixed?: boolean;
      mini?: boolean;
      mutex?: boolean;
      theme?: '#b7daff' | '#efdcde' | '#b3e0ca' | '#cbbdeb' | '#ffd8b8' | '#78b8ff';
    }
  
    interface AudioInfo {
      name?: string;
      artist?: string;
      url: string;
      cover?: string;
      lrc?: string;
    }
}
  